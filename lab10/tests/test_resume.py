from flask import url_for
from .base_test import BaseTest

class ResumeTest(BaseTest):
        
    def test_view_about_page(self):
        '''Tests an about page contains name'''

        response = self.client.get(url_for('resume.about_page'))   

        self.assert200(response)
        content = response.data.decode('utf-8')
        self.assertIn('Богдана Зарембовська', content)

    def test_view_skills_page(self):
        '''Tests a skills page contains some skills and image link'''

        response = self.client.get(url_for('resume.skills_page'))

        self.assert200(response)
        content = response.data.decode('utf-8')

        for skill in ["Data Science/Machine Learning", "Pandas/NumPy/SciPy/Matplotlib", "MySQL", "HTML &amp; CSS", "Jupyter Notebook", "Python", "OpenCV", "Deep Learning"]:
            self.assertIn(skill, content)

        image_link = url_for('static', filename='images/skills.jpg')
        self.assertIn(image_link.encode(), content.encode())

    def test_view_education_page(self):
        '''Tests the education page'''

        response = self.client.get(url_for('resume.education_page'))

        self.assert200(response)
        content = response.data.decode('utf-8')

        key_phrases = ["Мої дисципліни:", "Мій університет:"]
        for phrase in key_phrases:
            self.assertIn(phrase, content)