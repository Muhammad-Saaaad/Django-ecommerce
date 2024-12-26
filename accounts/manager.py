from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, username, password):
        if not username:
            raise ValueError("username not provided")
        if not password:
            raise ValueError("Password not provided")
        
        user = self.model(username= username)
        user.set_password(password)
        user.save(using= self.db)
        return user
    
    def create_superuser(self, username , password):
        user = self.create_user(username=username, password=password)
        user.is_admin=True
        user.is_staff=True
        user.is_superuser=True
        user.is_active=True
        user.save(using=self.db)
        return user
        