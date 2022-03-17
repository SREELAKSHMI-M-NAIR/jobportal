from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework import viewsets
from django.contrib.auth.models import User
from rest_framework.response import Response
# Create your views here.
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from  employer import serializers as sz
from employer.models import MyUser,CompanyProfile,Jobs,CandidateProfile


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = MyUser.objects.filter(role="employer")
    serializer_class = sz.CompanySerializer

    def create(self, request, *args, **kwargs):
        serializer=self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return  Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def list(self,request):
        employer=CompanyProfile.objects.all()
        serializer=sz.CompanySerializer(employer,many=True)
        return Response(serializer.data)






class CandidateViewSet(viewsets.ModelViewSet):
    queryset = MyUser.objects.filter(role="job_seeker")
    serializer_class = sz.CandidateSerializer

    def create(self, request, *args, **kwargs):
        serializer=self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return  Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


    @action(methods=["GET"], detail=False)
    def matching_jobs(self, request, *args, **kwargs):
        jobs = Jobs.objects.filter(skills__contains=request.user.candidate.skills)
        serializer = sz.JobSerializer(jobs, many=True)
        return Response(serializer.data)


class JobViewSet(viewsets.ModelViewSet):
    queryset = Jobs.objects.all()
    serializer_class = sz.JobSerializer
    permission_classes = [IsAuthenticated]


    def create(self, request, *args, **kwargs):
        serializer=self.serializer_class(data=request.data,context={"user":request.user})
        if serializer.is_valid():
            serializer.save()
            return  Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)