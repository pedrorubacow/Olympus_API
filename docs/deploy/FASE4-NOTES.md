# Fase 4 — Networking & Security — notas de decisão

**Sem dominio de teste disponivel**: HTTPS usa certificado self-signed
(gerado com `openssl req -x509`, comando documentado abaixo), nao Certbot/Let's
Encrypt de verdade. Navegador vai mostrar aviso de certificado nao confiavel —
esperado. Se um dominio real ficar disponivel no futuro, trocar por Certbot.

```bash
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout /etc/nginx/ssl/olympus-selfsigned.key \
  -out /etc/nginx/ssl/olympus-selfsigned.crt \
  -subj "/C=BR/ST=SP/O=OlympusAPI/CN=<IP-da-instancia>"
```

**SSH na porta 2222** (nao a 22 padrao): ver `sshd-hardening.conf`. Descoberta
relevante: uma vez que `sshd_config` tem QUALQUER linha `Port` explicita, o
padrao implicito (22) deixa de valer — o servico passa a escutar so nas portas
listadas.

**Flask isolada em 127.0.0.1:5000**: so o Nginx local fala com ela; nao esta
exposta externamente em nenhuma camada (nem ufw, nem security group, nem bind
de rede).

**Security group liberado por porta, nao por IP de origem**: tentamos
restringir por IP (o "meu IP" do Codespace), mas o Codespace usa um pool de
IPs de saida que ROTACIONA por conexao — um scan de portas confirmou isso
(algumas portas respondiam, outras nao, com a mesma regra). Restringir por IP
de origem so faz sentido quando o IP do cliente e estavel; aqui nao e.
Solucao: liberar exatamente as 3 portas necessarias (2222/80/443) pra
`0.0.0.0/0` no security group — e razoavel de qualquer forma, já que 80/443
precisam ser publicas e a defesa real do SSH e a chave, nao a origem do IP.

**Resultado do nmap** (todas as 65535 portas TCP escaneadas):
- Antes do ufw: so a porta 22 aberta (imagem limpa do Ubuntu).
- Depois de ufw + nginx + troca de porta do ssh: so 80, 443 e 2222 abertas.

**Drill de ataque simulado**: tentativa de login SSH so por senha (recusada),
tentativa de login como root (recusada), login por chave (funcionou).
