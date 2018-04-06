from ydk.services import CRUDService 
from ydk.providers import NetconfServiceProvider
from ydk.models.bgp import bgp


provider = NetconfServiceProvider(address=xrv, port=830, username=“cisco”, password=“cisco”, protocol=“ssh")

crud = CRUDService()  #  create  CRUD  service
bgp = bgp.Bgp() #  create oc bgp object
  #  set  local  AS  number
bgp.global_.config.router-id_ = "1.1.1.1"
crud.create(provider, bgp) #create  on  NETCONF  device
provider.close()

