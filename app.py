import streamlit as st
import pandas as pd
from datetime import datetime, date, time
from database import init_db, add_offer, get_offers, get_stats, update_status, import_offers, get_due_offers
from message import generate_message

st.set_page_config(page_title='PromoBox V3', page_icon='🔥', layout='wide')
init_db()

st.markdown('''<style>
.block-container{padding-top:1.5rem}.hero{padding:18px 22px;border-radius:18px;background:linear-gradient(135deg,#17142f,#24204d);border:1px solid #3b356d}.hero h1{margin:0}.small{opacity:.75}
</style>''', unsafe_allow_html=True)

st.markdown('<div class="hero"><h1>🔥 PromoBox V3</h1><div class="small">Central de ofertas • IA • importação • agendamento • canais</div></div>', unsafe_allow_html=True)

stats=get_stats()
cols=st.columns(5)
for c,label,key in zip(cols,['Ofertas','Programadas','Publicadas','Pendentes','Falhas'],['total','scheduled','published','pending','failed']):
    c.metric(label,stats[key])

menu=st.tabs(['➕ Oferta','📦 Gerenciar','📥 Importar','🤖 IA','📅 Agenda','📊 Estatísticas','⚙️ Configuração'])

with menu[0]:
    st.subheader('Cadastrar oferta')
    with st.form('new_offer',clear_on_submit=True):
        c1,c2=st.columns(2)
        with c1:
            name=st.text_input('Produto *')
            category=st.selectbox('Categoria',['Ofertas gerais','AutoPromoBox','Automotivo','Eletrônicos','Casa','Informática','Moda','Games'])
            old=st.number_input('Preço antigo',min_value=0.0,step=0.01)
            price=st.number_input('Preço promocional *',min_value=0.0,step=0.01)
        with c2:
            link=st.text_input('Link de afiliado *')
            image=st.text_input('URL da imagem')
            d=st.date_input('Data',value=date.today())
            t=st.time_input('Horário',value=time(9,0))
        extra=st.text_area('Observação para a IA')
        if st.form_submit_button('🔥 Cadastrar oferta',use_container_width=True):
            if not name or not link:
                st.error('Preencha produto e link.')
            else:
                add_offer(name,category,old,price,link,image,datetime.combine(d,t).isoformat(),extra)
                st.success('Oferta cadastrada.')

with menu[1]:
    offers=get_offers()
    if offers:
        for o in offers:
            with st.container(border=True):
                a,b,c=st.columns([4,2,1])
                with a:
                    st.markdown(f"### {o['name']}")
                    disc=((1-o['price']/o['old_price'])*100) if o['old_price'] and o['old_price']>o['price'] else 0
                    st.write(f"**{o['category']}** • R$ {o['price']:.2f}" + (f" • {disc:.0f}% OFF" if disc else ''))
                    st.caption(o['scheduled_at'])
                with b: st.write('Status:',o['status'])
                with c:
                    if o['status']!='publicada' and st.button('Publicar teste',key=f'p{o["id"]}'):
                        update_status(o['id'],'publicada'); st.rerun()
    else: st.info('Nenhuma oferta cadastrada.')

with menu[2]:
    st.subheader('Importar ofertas por CSV')
    st.write('Colunas aceitas: name, category, old_price, price, affiliate_url, image_url, scheduled_at, custom_text')
    file=st.file_uploader('Escolha um CSV',type=['csv'])
    if file:
        df=pd.read_csv(file)
        st.dataframe(df,use_container_width=True)
        if st.button('📥 Importar CSV'):
            required=['name','price','affiliate_url']
            missing=[x for x in required if x not in df.columns]
            if missing: st.error('Faltam colunas: '+', '.join(missing))
            else:
                n=import_offers(df.to_dict('records')); st.success(f'{n} ofertas importadas.')

with menu[3]:
    st.subheader('🤖 Gerar texto promocional com IA')
    offers=get_offers()
    if not offers: st.info('Cadastre uma oferta primeiro.')
    else:
        names=[f"#{o['id']} — {o['name']}" for o in offers]
        selected=st.selectbox('Oferta',names)
        oid=int(selected.split('—')[0].replace('#','').strip())
        offer=next(o for o in offers if o['id']==oid)
        tone=st.selectbox('Estilo',['Urgente','Direto','Divertido','Profissional'])
        if st.button('✨ Gerar mensagem'):
            st.code(generate_message(offer,tone),language=None)
            st.caption('Se OPENAI_API_KEY estiver configurada, o gerador usa IA; caso contrário, usa o gerador local.')

with menu[4]:
    st.subheader('📅 Agenda')
    due=get_due_offers()
    if due: st.warning(f'{len(due)} oferta(s) já estão no horário de processamento.')
    df=pd.DataFrame(get_offers())
    if not df.empty:
        df['scheduled_at']=pd.to_datetime(df['scheduled_at'],errors='coerce')
        st.dataframe(df[['id','name','category','scheduled_at','status']],use_container_width=True)
    st.info('O worker verifica a agenda a cada 60 segundos. Para hospedagem, use um serviço externo de execução contínua/cron para o worker; o Streamlit sozinho não é um agendador persistente.')

with menu[5]:
    st.subheader('📊 Estatísticas')
    st.bar_chart(pd.DataFrame({'Status':['Programadas','Publicadas','Falhas'],'Quantidade':[stats['scheduled'],stats['published'],stats['failed']]}).set_index('Status'))

with menu[6]:
    st.subheader('⚙️ Configuração')
    st.info('As credenciais devem ser configuradas em Secrets/variáveis de ambiente, nunca no GitHub.')
    st.code('OPENAI_API_KEY = "..."\nOPENAI_MODEL = "..."\nPUBLISH_WEBHOOK_URL = "..."',language='toml')
    st.markdown('**Canais preparados:** adaptador de webhook e estrutura para integração oficial/permitida de WhatsApp ou outro canal.')
