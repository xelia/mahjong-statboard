from django import forms
from django.contrib import admin

from . import models


class InstanceDomainInline(admin.TabularInline):
    model = models.InstanceDomain
    extra = 0


@admin.register(models.Instance)
class InstanceAdmin(admin.ModelAdmin):
    inlines = (InstanceDomainInline, )
    list_display = ('name', 'domains')

    def domains(self, obj):
        return ', '.join(d.name for d in obj.domains.all())

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


@admin.register(models.Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('name', 'full_name', 'instance', 'hidden', )
    readonly_fields = ('instance',)
    search_fields = ('name', )

    def has_module_permission(self, request):
        return request.user.is_superuser or not request.user.is_anonymous and request.user.instance_set.count()

    def has_change_permission(self, request, obj=None):
        if obj:
            return request.user.is_superuser or request.user in obj.instance.admins.all()
        return True

    def has_delete_permission(self, request, obj=None):
        if obj:
            return request.user.is_superuser or request.user in obj.instance.admins.all()
        return True

    def get_queryset(self, request):
        if request.user.is_superuser:
            qs = models.Player.objects.all()
        else:
            qs = models.Player.objects.filter(instance__admins=request.user)
        return qs


class GameResultsFormSet(forms.BaseInlineFormSet):
    def clean(self):
        super().clean()
        score_sum = 0
        starting_positions = set()
        players = set()
        for form in self.forms:
            form.cleaned_data['place'] = 4
            score_sum += form.cleaned_data['score']
            players.add(form.cleaned_data['player'])
            starting_positions.add(form.cleaned_data['starting_position'])
        if score_sum != 100000:
            raise forms.ValidationError('Score sum is {}'.format(score_sum))
        if starting_positions != {1, 2, 3, 4}:
            raise forms.ValidationError('Bad starting positions')
        if len(players) != 4:
            raise forms.ValidationError('Players is not unique')


class GameResultInline(admin.TabularInline):
    model = models.GameResult
    list_filter = (('instance', admin.RelatedOnlyFieldListFilter),)
    fields = ('player', 'score', 'place', 'starting_position')
    readonly_fields = ('place', )
    extra = 0
    max_num = 4
    min_num = 4
    formset = GameResultsFormSet

    def has_change_permission(self, request, obj=None):
        if obj:
            return request.user.is_superuser  # or request.user in obj.instance.admins.all()
        return True

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(models.Game)
class GamesAdmin(admin.ModelAdmin):
    inlines = (GameResultInline, )
    list_display = ('instance', 'date', 'addition_time', 'result')
    readonly_fields = list_display + ('posted_by', )

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        form.instance.recount_places()

    def result(self, obj):
        return ' '.join('{}:{}'.format(gr.player.name, gr.score) for gr in obj.gameresult_set.all())

    def has_module_permission(self, request):
        return request.user.is_superuser  # or not request.user.is_anonymous and request.user.instance_set.count()

    def has_change_permission(self, request, obj=None):
        if obj:
            return request.user.is_superuser or request.user in obj.instance.admins.all()
        return True

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def get_queryset(self, request):
        if request.user.is_superuser:
            qs = models.Game.objects.all()
        else:
            qs = models.Game.objects.filter(instance__admins=request.user)
        qs = qs.prefetch_related('gameresult_set', 'gameresult_set__player')
        return qs
