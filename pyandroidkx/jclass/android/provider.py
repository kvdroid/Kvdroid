from jnius import autoclass

Provider = autoclass('android.provider.Settings')
Contacts = autoclass('android.provider.ContactsContract$Contacts')
Phone = autoclass('android.provider.ContactsContract$CommonDataKinds$Phone')
