import time
from database import init_db,get_due_offers,update_status
from message import generate_message
from sender import send_offer

init_db(); print('🔥 PromoBox worker iniciado')
while True:
    for o in get_due_offers():
        msg=generate_message(o,'Direto')
        ok,detail=send_offer(msg,o['image_url'] or '')
        if ok: update_status(o['id'],'publicada'); print('Publicado:',o['name'])
        else: print('Não enviado:',o['name'],detail)
    time.sleep(60)
