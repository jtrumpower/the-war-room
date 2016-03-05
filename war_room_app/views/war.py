from war_room_app.models import War
from war_room_app.models import Member
from war_room_app.models import Clan
from war_room_app.models import Base
from war_room_app.serializers import WarSerializer
from rest_framework import generics
from war_room_app.clash_api import clans
from rest_framework.renderers import JSONRenderer
from war_room_app.exceptions import CouldntRetrieveClan
from rest_framework import viewsets
from rest_framework.response import Response
import urllib
import logging


class WarList(generics.ListCreateAPIView):
    queryset = War.objects.all()
    serializer_class = WarSerializer

    def perform_create(self, serializer):
        clanResponse = clans.get_clan_by_tag(urllib.quote_plus(serializer.validated_data.get('clan_tag')))
        enemyClanResponse = clans.get_clan_by_tag(urllib.quote_plus(serializer.validated_data.get('enemy_clan_tag')))

        if clanResponse.status_code == 404:
            raise CouldntRetrieveClan(detail="No Results for your clan tag")

        if enemyClanResponse.status_code == 404:
            raise CouldntRetrieveClan(detail="No Results for enemy clan tag")

        clan = clanResponse.json()
        enemyClan = enemyClanResponse.json()

        myClanTag = serializer.validated_data.get('clan_tag')[1:]
        enemyClanTag = serializer.validated_data.get('enemy_clan_tag')[1:]

        myClan = Clan.objects.filter(clan_tag=myClanTag)
        if len(myClan) == 1:
            myClan = myClan[0];
        elif len(myClan) > 1:
            raise CouldntRetrieveClan(detail="Not a unique clan tag")
        else:
            myClan = Clan(name=clan.get('name'), clan_tag=clan.get("tag")[1:])
            myClan.save()

        serializer.validated_data['title'] = "{0} Vs {1}".format(clan.get('name'), enemyClan.get('name'))
        serializer.validated_data['clan_id'] = myClan.clan_tag
        members = clan.get('memberList')
        if members != None:
            for clan_member in members:
                mem = Member.objects.filter(game_name=clan_member.get('name'), clan_tag=myClan)
                if len(mem) == 0:
                    m = Member(game_name=clan_member.get('name'), clan_tag=myClan)
                    m.save()

        print serializer.validated_data.get('clan_tag')
        print serializer.validated_data.get('clan_id')
        war = serializer.save()

        enemyMembers = enemyClan.get('memberList')
        if enemyMembers != None:
            for clan_member in enemyMembers:
                m = Base(war=war, name = clan_member.get('name'))
                m.save()
        return war


class WarDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = War.objects.all()
    serializer_class = WarSerializer


class WarByClan(viewsets.ViewSet):

    def get_all_wars(self, request, clan_tag):
        queryset = War.objects.filter(clan=clan_tag)
        serializer = WarSerializer(queryset, many=True)
        return Response(serializer.data)

    def get_by_clan(self, request, clan_tag, war_id):
        queryset = War.objects.get(pk=war_id, clan=clan_tag)
        serializer = WarSerializer(queryset)
        return Response(serializer.data)

    def get_latest_by_clan(self, request, clan_tag):
        queryset = War.objects.filter(clan=clan_tag).latest()
        serializer = WarSerializer(queryset)
        return Response(serializer.data)

