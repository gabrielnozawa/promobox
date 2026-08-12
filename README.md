# 🔥 PromoBox V3

Painel de automação de ofertas com cadastro, importação CSV, IA opcional, agenda e adaptador de publicação por webhook.

## Rodar localmente
```bash
python -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements.txt
streamlit run app.py
```

Worker:
```bash
python worker.py
```

## IA
Configure `OPENAI_API_KEY` e opcionalmente `OPENAI_MODEL` em Secrets/variáveis de ambiente. Sem chave, o sistema usa um gerador local e continua funcionando.

## Importação
Use CSV com pelo menos:
`name,price,affiliate_url`

Também aceita:
`category,old_price,image_url,scheduled_at,custom_text`

## Publicação
`sender.py` usa um webhook configurável. Isso deixa a integração desacoplada. Para WhatsApp, conecte uma API oficial/permitida que aceite o destino e o tipo de mensagem desejados. Não use automação de cliques do WhatsApp Web.

## Deploy no Streamlit
Entrypoint: `app.py`.
Para produção, o worker deve rodar em um serviço de execução contínua/cron separado do Streamlit.
