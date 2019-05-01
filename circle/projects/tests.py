from django.conf import settings
from django.test import TestCase
from .accounts import views
from .accounts import models
# May have to import User from settings...?
# May have to doublecheck syntax for import from accounts app.


# Circle Projects Tests
class ModelSetUp(object):
    def setUp(self):
        # 1. Account Models
        # User Models
        self.user1 = settings.AUTH_USER_MODEL(
            email='user1@example.com',
            username='User1',
            display_name='User_1',
            bio='User1 Bio',
            avatar=None,
            is_staff=True
        )
        self.user1.save()

        # Skill Models
        self.skill1 = Skill(
            name='Skill1',
        )
        self.skill1.save()
        self.skill1.users = (
            self.user1,
            self.user2,
            self.user3
        )
        self.skill1.save()

        # 2. Project Models
        # Project Models
        # With no name default should either be "Project 1" or "Project 0".
        self.proj1 = models.Project(
            description='Project1 Description',
            creator=self.user1
        )

        # Position Models
        self.posi1 = models.Position(
            name='Job1',
            description='Job1desc',
            project=self.proj1,
            user=self.user1,
        )
        self.posi1.save()
        self.posi1.skills = (
            self.skill1,
            self.skill2,
            self.skill3
        )
        self.posi1.save()
    
        # Applicant Models
        self.appl1 = models.Applicant(
            user=self.user1,
            position=self.posi1
        )
        self.appl1.save()


class TemplateSetUp(object):
    pass


class ViewSetUp(object):
    pass


class ProjectModelTests(ModelSetUp, TestCase):
    '''Project model tests.'''
    def test_user_creation(self):
        self.assertEqual(self.user1.username, 'User1')
        self.assertNotEqual(self.user1.email, self.user2.email)
        self.assertLessEqual(self.user1.date_joined, timezone.now())

    def test_skill_creation(self):
        self.assertEqual(self.skill1.name, 'Skill1')
        self.assertNotEqual(self.skill1.name, self.skill2.name)
        self.assertIn(self.skill1.users, self.user1)

    def test_applicant_creation(self):
        self.assertEqual(self.appl1.user, self.user1)
        self.assertEqual(self.appl1.position, self.posi1)
        self.assertLessEqual(self.appl1.applied, timezone.now())
        self.assertEqual(self.appl1.status, True)

    def test_position_creation(self):
        self.assertEqual(self.posi1.name, 'Job1')
        self.assertEqual(self.posi1.project, self.proj1)
        self.assertEqual(self.posi1.user, self.user1)
        self.assertIn(self.posi1.skills, self.skill1)

    def test_project_creation(self):
        self.assertEqual(self.proj1.name, 'Project 1')
        self.assertNotEqual(self.proj1.name, self.proj2.name)
        self.assertEqual(self.proj1.creator.name, 'User1')


class ProjectTemplateTests(TemplateSetUp, ViewSetUp, ModelSetUp, TestCase):
    pass


class ProjectViewTests(ViewSetUp, ModelSetUp, TestCase):
    pass
