from django.contrib import admin

from . import models


@admin.register(models.Instance)
class InstanceAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return request.user.is_superuser or not request.user.is_anonymous and request.user.instance_set.count()

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        if obj:
            return request.user.is_superuser or request.user in obj.admins.all()
        return True

    def get_queryset(self, request):
        if request.user.is_superuser:
            return models.Instance.objects.all()
        else:
            return models.Instance.objects.filter(admins=request.user)


@admin.register(models.Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('instance', 'rating_name', 'rating_type_id', 'series_len', 'start_date', 'end_date', 'weight', 'state')
    list_editable = ('weight', 'state')
    list_filter = (('instance', admin.RelatedOnlyFieldListFilter),)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not request.user.is_superuser:
            form.base_fields['instance'].queryset = models.Instance.objects.filter(admins=request.user)
        return form

    def has_module_permission(self, request):
        return request.user.is_superuser or not request.user.is_anonymous and request.user.instance_set.count()

    def has_add_permission(self, request):
        return request.user.is_superuser or request.user.instance_set.count()

    def has_delete_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        if obj:
            return request.user.is_superuser or request.user in obj.instance.admins.all()
        return True

    def get_queryset(self, request):
        if request.user.is_superuser:
            return models.Rating.objects.all()
        else:
            return models.Rating.objects.filter(instance__admins=request.user)


@admin.register(models.Stats)
class StatsAdmin(admin.ModelAdmin):
    list_filter = (('rating', admin.RelatedOnlyFieldListFilter),)
    list_display = ('instance', 'rating', 'player', 'value', 'game', 'place')
    readonly_fields = list_display

    def has_module_permission(self, request):
        return request.user.is_superuser or not request.user.is_anonymous and request.user.instance_set.count()

    def has_change_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_queryset(self, request):
        if request.user.is_superuser:
            return models.Stats.objects.all()
        else:
            return models.Stats.objects.filter(instance__admins=request.user)