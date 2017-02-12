from django.contrib import admin

from polls.models import Place, Candidate, Election, Result, \
    TrendSource, Trend, Party, PoliticalFunction, Role, \
    DetailedResults


class CandidateAdmin(admin.ModelAdmin):
    fields = ('name', 'surname', 'birth_date', 'birth_place', 'nationality', 'image_url')
    list_display = fields


class ElectionAdmin(admin.ModelAdmin):
    fields = ('name', 'date', 'place',)
    list_display = fields


class PlaceAdmin(admin.ModelAdmin):
    fields = ('country', 'region', 'department', 'county', 'city')
    list_display = fields


class ResultAdmin(admin.ModelAdmin):
    fields = ('candidate', 'election', 'voting_result')
    list_display = ('candidate', 'election_name', 'voting_result')

    def election_name(self, obj):
        return obj.election.print_name


class RoleAdmin(admin.ModelAdmin):
    fields = ('candidate', 'short_position_type', 'election', 'beginning_date', 'end_date')
    list_display = fields

    def short_position_type(self, obj):
        return obj.position_type.short_description


class TrendSourceAdmin(admin.ModelAdmin):
    fields = ('name', 'grade')
    list_display = fields


class TrendAdmin(admin.ModelAdmin):
    fields = ('election', 'candidate', 'score', 'weight', 'trend_source', 'date', 'place')
    list_display = ('election_name', 'candidate', 'score', 'weight', 'trend_source', 'date')

    def election_name(self, obj):
        return obj.election.print_name

admin.site.register(Candidate, CandidateAdmin)
admin.site.register(Election, ElectionAdmin)
admin.site.register(Place, PlaceAdmin)
admin.site.register(Result, ResultAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(TrendSource, TrendSourceAdmin)
admin.site.register(Trend, TrendAdmin)

admin.site.register(Party)
admin.site.register(PoliticalFunction)
admin.site.register(DetailedResults)
