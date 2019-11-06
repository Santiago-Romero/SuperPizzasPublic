from rolepermissions.roles import AbstractUserRole

class Administrador(AbstractUserRole):
    available_permissions = {
        
    }

class Auxiliar(AbstractUserRole):
    available_permissions = {
        
    }
    
class Cliente(AbstractUserRole):
    available_permissions = {
        
    }
    
class Vendedor(AbstractUserRole):
    available_permissions = {
        
    }