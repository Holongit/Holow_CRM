from django.contrib import admin

from workers.models import Workers, KartkaGwarancja, KartkaPlatne, KartkaReklamacja, KartkaRezygnacja

admin.site.register(Workers)
admin.site.register(KartkaReklamacja)
admin.site.register(KartkaRezygnacja)
admin.site.register(KartkaPlatne)
admin.site.register(KartkaGwarancja)




