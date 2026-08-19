# Fase 5 — Server Management: notas e decisões

## Arquitetura escolhida
1 EC2 t3.micro (`us-east-1`) rodando 3 processos da Olympus API em portas
diferentes (5001/5002/5003), com Nginx na mesma máquina fazendo o papel de
load balancer. Optamos por isso em vez de 2-3 EC2s separadas porque a conta
não está mais no free tier — uma instância só (e um volume EBS só) minimiza
a superfície de custo. O Nginx não se importa se os backends estão no mesmo
host ou em hosts diferentes; a sintaxe do `upstream` é idêntica.

## O que foi construído
- **systemd template unit** (`/etc/systemd/system/olympus-api@.service`,
  versionado em `deploy/olympus-api@.service`): usa `%i` como a porta,
  então `systemctl enable --now olympus-api@5001/5002/5003` sobe três
  processos independentes reaproveitando o mesmo arquivo de unit — sem
  duplicar nada.
- **Nginx dividido em duas partes**: `docs/deploy/nginx-olympus-api.conf`
  (estático — redirect 80→443, SSL self-signed, rotas, cache) e
  `docs/deploy/nginx-upstream.conf` (o bloco `upstream`, que muda toda vez
  que adicionamos/removemos uma instância). O upstream vive em
  `/etc/nginx/conf.d/`, que o `nginx.conf` já inclui automaticamente.
- **`scripts/generate-nginx-lb.sh`**: recebe a lista de portas via `-p`,
  regenera só o arquivo de upstream, roda `nginx -t` antes de qualquer
  coisa, e só dá `reload` se a config for válida — se for inválida, o
  Nginx antigo continua rodando intocado. Usado pra adicionar a 3ª
  instância sem editar nada na mão.
- **Cache** na rota de listagem (`/gods`, `/creatures`, `/myths`, via
  regex `location`), 30s de TTL, `proxy_cache_path` registrado no bloco
  `http` do `nginx.conf`. Rota `/quiz` fica de fora do cache de propósito
  (é aleatória, cachear destruiria o propósito dela).
- **Headers de verificação**: `X-Cache-Status` (HIT/MISS) e
  `X-Upstream-Addr` (qual backend respondeu) adicionados nas respostas —
  é assim que provamos round-robin e cache funcionando de fora, sem
  precisar olhar log no servidor.

## Critério de pronto: confirmado
- Round-robin confirmado nas 3 portas via `X-Upstream-Addr` alternando
  5001→5002→5003 em requisições sucessivas ao `/quiz`.
- Cache confirmado via `X-Cache-Status`: 1ª request em `/gods` = `MISS`
  (com `X-Upstream-Addr` preenchido), requests seguintes dentro dos 30s =
  `HIT` (sem `X-Upstream-Addr`, porque nem chegou a sair do Nginx).
- Drill de failover: `systemctl stop olympus-api@5001` com tráfego
  contínuo rodando — zero request falhou, uma única request de transição
  mostrou `X-Upstream-Addr: 127.0.0.1:5001, 127.0.0.1:5002` (o Nginx
  tentou a porta morta, falhou, tentou a próxima automaticamente, dentro
  da mesma requisição), depois disso 100% do tráfego foi só pra 5002 até
  a 5001 voltar.

## Bugs e lições reais (vale lembrar o padrão)
1. **Security group esquecido**: copiamos o padrão final da Fase 4
   (2222/80/443) pra essa EC2 nova, mas essa instância crua ainda não
   tinha o hardening SSH aplicado — o SSH dela ainda escuta na porta 22
   padrão. `ssh` ficou travado em timeout silencioso (não recusa, só não
   responde) até liberarmos a 22 também no security group. Lição: o
   security group "final" de uma fase anterior não é o security group
   "inicial" de uma instância nova.
2. **Chave privada rsyncada sem querer**: o primeiro `rsync` do código
   pro servidor levou junto o `olympus-fase5-key.pem` (a chave que abre a
   própria EC2), porque ele mora na raiz do repo e não tinha regra de
   `.gitignore`. Corrigido: chave removida do servidor, `*.pem` adicionado
   ao `.gitignore` pra não repetir isso (e pra nunca virar risco de vazar
   no histórico do Git).
3. **Banco vazio em infra nova**: o `/quiz` respondia `400` numa EC2 recém
   criada — não era bug, era o `rsync` corretamente excluindo o banco
   antigo (`instance/olympus.db`) e a validação da própria app funcionando
   como esperado (sem dado, sem quiz). Resolvido populando alguns
   registros de teste via `POST` antes de validar o resto da fase.
4. **Variáveis de shell não sobrevivem entre sessões de terminal**: mais
   um lembrete (já visto na Fase 2) de por que automação de verdade vai
   pra dentro de um script versionado, não em comandos colados direto no
   terminal interativo — foi exatamente o motivo de escrevermos o
   `generate-nginx-lb.sh` em vez de continuar editando a config na mão.

## Limpeza pendente
EC2 (`i-0c018e130e37ce58e`) e security group (`sg-0d9c674487f12fc60`)
devem ser **terminados** (não só parados) depois do merge do PR — mesmo
padrão das Fases 3 e 4, pra não sobrar EBS cobrando à toa.
