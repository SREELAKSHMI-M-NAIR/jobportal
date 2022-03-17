from rest_framework.serializers import ModelSerializer
from employer.models import MyUser,Jobs,CandidateProfile,CompanyProfile


class CompanyProfileSerializer(ModelSerializer):
    class Meta:
        model = CompanyProfile
        fields = [
            "company_name",
            "description",
        ]


class CompanySerializer(ModelSerializer):
    profile = CompanyProfileSerializer(required=True)

    class Meta:
        model = MyUser
        fields = ["email", "password", "role", "profile", "phone"]

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')

        password = validated_data.pop('password')
        user = MyUser(**validated_data)
        user.set_password(password)
        user.save()
        CompanyProfile.objects.create(company=user, **profile_data)
        return user


class CandidateProfileSerializer(ModelSerializer):
    class Meta:
        model = CandidateProfile
        fields = [
            "name",
            "qualification",
            "experience",
            "skills"
        ]


class CandidateSerializer(ModelSerializer):
    profile = CandidateProfileSerializer(required=True)

    class Meta:
        model = MyUser
        fields = ["email", "password", "role", "profile", "phone"]

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')

        password = validated_data.pop('password')
        user = MyUser(**validated_data)
        user.set_password(password)
        user.save()
        CompanyProfile.objects.create(company=user, **profile_data)
        return user



class JobSerializer(ModelSerializer):
    class Meta:
        model=Jobs
        fields=[
            "post_name",
            "experience",
            "skills",
            "description"

        ]

    def create(self, validated_data):
        job = Jobs(**validated_data, company=self.context["user"])

        job.save()
        return job