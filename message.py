import os

def local_message(o,tone='Direto'):
    old=o['old_price']; price=o['price']; disc=((1-price/old)*100) if old and old>price else 0
    opener={'Urgente':'🚨 CORRE! OFERTA POR TEMPO LIMITADO!','Direto':'🔥 OFERTA DO DIA!','Divertido':'👀 OLHA ESSA OFERTA!','Profissional':'⭐ Oferta em destaque'}[tone]
    lines=[opener,'',f"🛍️ *{o['name']}*"]
    if old and old>price: lines += [f'~~De R$ {old:.2f}~~',f'💰 *Por R$ {price:.2f}*',f'🏷️ *{disc:.0f}% OFF*']
    else: lines += [f'💰 *R$ {price:.2f}*']
    if o['custom_text']: lines += ['',o['custom_text']]
    lines += ['','🛒 Confira:',o['affiliate_url'],'','⚠️ Preço e disponibilidade podem mudar.']
    return '\n'.join(lines)

def generate_message(o,tone='Direto'):
    key=os.getenv('OPENAI_API_KEY')
    if not key: return local_message(o,tone)
    try:
        from openai import OpenAI
        client=OpenAI(api_key=key)
        model=os.getenv('OPENAI_MODEL')
        prompt=f'''Crie uma mensagem curta de oferta para WhatsApp em português do Brasil. Seja persuasivo sem inventar informações. Produto: {o['name']}. Preço antigo: {o['old_price']}. Preço atual: {o['price']}. Categoria: {o['category']}. Observação: {o['custom_text']}. Estilo: {tone}. Inclua o link exatamente no final: {o['affiliate_url']}'''
        kwargs={'model':model,'input':prompt}
        if model: kwargs['model']=model
        r=client.responses.create(**kwargs)
        return r.output_text
    except Exception:
        return local_message(o,tone)
