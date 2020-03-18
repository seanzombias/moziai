from MoziService import MoZiPython
from MoziService.entitys import satellite

server_ip = '127.0.0.1'
server_port = 6260

# {name='猎户座USA110军事卫星', guid='649ea076-fbeb-414e-8841-0a2aa9e62a2d'}
name='猎户座USA110军事卫星'
guid='649ea076-fbeb-414e-8841-0a2aa9e62a2d'
side_name = '红方'
mozi_task = MoZiPython.MoZi(server_ip, server_port)
sat = satellite.Csatellite(guid, name, side_name, mozi_task)

def test_sate_set_rader_shutdown():
    trunoff=True
    ret = sat.sate_set_rader_shutdown(trunoff)
    print(ret)

def test_sate_set_sonar_shutdown():
    trunoff=True
    ret = sat.sate_set_sonar_shutdown(trunoff)
    print(ret)

def test_sate_set_OECM_shutdown():
    trunoff=True
    ret = sat.sate_set_OECM_shutdown(trunoff)
    print(ret)




def test():
    # test_sate_set_rader_shutdown()
    # test_sate_set_sonar_shutdown()
    test_sate_set_OECM_shutdown()

test()