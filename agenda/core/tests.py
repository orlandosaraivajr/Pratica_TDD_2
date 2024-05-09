from django.test import TestCase
from django.shortcuts import resolve_url as r
from django.db.models.query import QuerySet
from core.models import AgendaModel
from core.forms import AgendaForm


class Index_GET_POST_Test(TestCase):
    def setUp(self):
        self.resp = self.client.get(r('core:index'), follow=True)
        self.resp_post = self.client.post(r('core:index'))

    def test_status_code(self):
        self.assertEqual(self.resp.status_code , 200)
        self.assertEqual(self.resp_post.status_code , 302)
    
    def test_template_used(self):
        self.assertTemplateUsed(self.resp, 'index.html')

    def test_found_html(self):
        tags = (
            ('<html', 1),
            ('<body>', 1),
            ('Cadastro de Pessoas', 1),
            ('Agenda Pessoal', 1),
            ('<input', 4),
            ('<br>', 5),
            ('</body>', 1),
            ('</html>', 1),
        )
        for text, count in tags:
            with self.subTest():
                self.assertContains(self.resp, text, count)


class AgendaModelTest(TestCase):
    def setUp(self):
        self.agenda = AgendaModel(
            nome='José da Silva',
            telefone='9999999999',)
        self.agenda.save()

    def test_str(self):
        self.assertEqual(str(self.agenda), 'José da Silva')

    def test_created(self):
        self.assertTrue(AgendaModel.objects.exists())

    def test_data_saved(self):
        data = AgendaModel.objects.first()
        self.assertEqual(data.nome, 'José da Silva')
        self.assertEqual(data.telefone, '9999999999')


class AgendaFormTest(TestCase):
    def test_unbounded_fields(self):
        form = AgendaForm()
        expected = ['nome', 'telefone']
        self.assertSequenceEqual(expected, list(form.fields))

    def test_form_all_OK(self):
        dados = dict(nome='José da Silva', telefone='1999998888')
        form = AgendaForm(dados)
        errors = form.errors
        self.assertEqual({}, errors)
        self.assertEqual(form.cleaned_data['nome'], 'JOSÉ DA SILVA')

    def test_form_wrong_DDD(self):
        dados = dict(nome='José da Silva', telefone='9999998888')
        form = AgendaForm(dados)
        errors = form.errors
        errors_list = errors['telefone']
        msg = 'DDD válido somente o 19'
        self.assertEqual([msg], errors_list)

    def test_form_no_name(self):
        dados = dict(telefone='1999998888')
        form = AgendaForm(dados)
        errors = form.errors
        errors_list = errors['nome']
        msg = 'This field is required.'
        self.assertEqual([msg], errors_list)
    
    def test_form_no_phone(self):
        dados = dict(nome='José da Silva')
        form = AgendaForm(dados)
        errors = form.errors
        errors_list = errors['telefone']
        msg = 'This field is required.'
        self.assertEqual([msg], errors_list)


class Create_GET_Test(TestCase):
    def setUp(self):
        self.resp = self.client.get(r('core:create'), follow=True)

    def test_status_code(self):
        self.assertEqual(self.resp.status_code , 200)
  
    def test_context(self):
        form_used = self.resp.context['form']
        self.assertIsInstance(form_used, AgendaForm)
          
    def test_template_used(self):
        self.assertTemplateUsed(self.resp, 'cadastro.html')


class Create_POST_OK_Test(TestCase):
    def setUp(self):
        data = {'nome': 'José da Silva',
                'telefone': '1988887777',}
        self.resp = self.client.post(r('core:create'), data, follow=True)
        self.resp2 = self.client.post(r('core:create'), data)

    def test_status_code(self):
        self.assertEqual(self.resp.status_code , 200)
        self.assertEqual(self.resp2.status_code , 302)
  
    def test_template_used(self):
        self.assertTemplateUsed(self.resp, 'index.html')


class Create_POST_Fail_Test(TestCase):
    def setUp(self):
        data = {'nome': 'José da Silva',
                'telefone': '9988887777',}
        self.resp = self.client.post(r('core:create'), data, follow=True)
        self.resp2 = self.client.post(r('core:create'), data)

    def test_status_code(self):
        self.assertEqual(self.resp.status_code , 200)
        self.assertEqual(self.resp2.status_code , 200)
  
    def test_context(self):
        form_used = self.resp.context['form']
        self.assertIsInstance(form_used, AgendaForm)
          
    def test_template_used(self):
        self.assertTemplateUsed(self.resp, 'cadastro.html')


class Read_GET_Test(TestCase):
    def setUp(self):
        self.resp = self.client.get(r('core:read'), follow=True)

    def test_status_code(self):
        self.assertEqual(self.resp.status_code , 200)
  
    def test_context(self):
        form_used = self.resp.context['contatos']
        self.assertIsInstance(form_used, QuerySet)
          
    def test_template_used(self):
        self.assertTemplateUsed(self.resp, 'listar.html')


class Read_POST_OK_Test(TestCase):
    def setUp(self):
        data = {'nome': 'José da Silva',
                'telefone': '1988887777',}
        AgendaModel.objects.create(**data)
        data = {'id':1}
        self.resp = self.client.post(r('core:read'), data, follow=True)
        self.resp2 = self.client.post(r('core:read'), data)

    def test_status_code(self):
        self.assertEqual(self.resp.status_code , 200)
        self.assertEqual(self.resp2.status_code , 200)
  
    def test_template_used(self):
        self.assertTemplateUsed(self.resp, 'detalhes.html')

    def test_found_html(self):
        tags = (
            ('<html', 1),
            ('<body>', 1),
            ('Cadastro de Pessoas', 1),
            ('Agenda Pessoal', 1),
            ('José da Silva', 1),
            ('</body>', 1),
            ('</html>', 1),
        )
        for text, count in tags:
            with self.subTest():
                self.assertContains(self.resp, text, count)


class Read_POST_Fail_Test(TestCase):
    def setUp(self):
        data = {'nome': 'José da Silva',
                'telefone': '1988887777',}
        AgendaModel.objects.create(**data)
        data = {}
        self.resp = self.client.post(r('core:read'), data, follow=True)
        self.resp2 = self.client.post(r('core:read'), data)

    def test_status_code(self):
        self.assertEqual(self.resp.status_code , 200)
        self.assertEqual(self.resp2.status_code , 200)
  
    def test_template_used(self):
        self.assertTemplateUsed(self.resp, 'detalhes.html')

    def test_found_html(self):
        tags = (
            ('<html', 1),
            ('<body>', 1),
            ('Cadastro de Pessoas', 1),
            ('Agenda Pessoal', 1),
            ('Nenhum contato cadastrado', 1),
            ('</body>', 1),
            ('</html>', 1),
        )
        for text, count in tags:
            with self.subTest():
                self.assertContains(self.resp, text, count)
    

class Update_GET_Test(TestCase):
    def setUp(self):
        self.resp = self.client.get(r('core:update'), follow=True)

    def test_status_code(self):
        self.assertEqual(self.resp.status_code , 200)
  
    def test_context(self):
        form_used = self.resp.context['contatos']
        self.assertIsInstance(form_used, QuerySet)
          
    def test_template_used(self):
        self.assertTemplateUsed(self.resp, 'atualizar.html')


class Update_POST_OK_Test(TestCase):
    def setUp(self):
        data = {'nome': 'José da Silva',
                'telefone': '1988887777',}
        AgendaModel.objects.create(**data)
        data = {'id':1}
        self.resp = self.client.post(r('core:update'), data, follow=True)
        self.resp2 = self.client.post(r('core:update'), data)

    def test_status_code(self):
        self.assertEqual(self.resp.status_code , 200)
        self.assertEqual(self.resp2.status_code , 200)
  
    def test_template_used(self):
        self.assertTemplateUsed(self.resp, 'atualizar2.html')

    def test_found_html(self):
        tags = (
            ('<html', 1),
            ('<body>', 1),
            ('Cadastro de Pessoas', 1),
            ('Agenda Pessoal', 1),
            ('José da Silva', 1),
            ('</body>', 1),
            ('</html>', 1),
        )
        for text, count in tags:
            with self.subTest():
                self.assertContains(self.resp, text, count)


class Update_POST_Fail_Test(TestCase):
    def setUp(self):
        data = {'nome': 'José da Silva',
                'telefone': '1988887777',}
        AgendaModel.objects.create(**data)
        data = {}
        self.resp = self.client.post(r('core:update'), data, follow=True)
        self.resp2 = self.client.post(r('core:update'), data)

    def test_status_code(self):
        self.assertEqual(self.resp.status_code , 200)
        self.assertEqual(self.resp2.status_code , 200)
  
    def test_template_used(self):
        self.assertTemplateUsed(self.resp, 'atualizar2.html')

    def test_found_html(self):
        tags = (
            ('<html', 1),
            ('<body>', 1),
            ('Cadastro de Pessoas', 1),
            ('Agenda Pessoal', 1),
            ('Nenhum contato cadastrado', 1),
            ('</body>', 1),
            ('</html>', 1),
        )
        for text, count in tags:
            with self.subTest():
                self.assertContains(self.resp, text, count)


class Confirm_Update_GET_Test(TestCase):
    def setUp(self):
        self.resp = self.client.get(r('core:confirm_update'), follow=True)

    def test_status_code(self):
        self.assertEqual(self.resp.status_code , 200)
          
    def test_template_used(self):
        self.assertTemplateUsed(self.resp, 'index.html')


class Confirm_Update_POST_OK_Test(TestCase):
    def setUp(self):
        data = {'nome': 'José da Silva',
                'telefone': '1988887777',}
        AgendaModel.objects.create(**data)
        data = {'nome': 'Maria José',
                'telefone': '19666667777','id':1}
        self.resp = self.client.post(r('core:confirm_update'), data, follow=True)
        self.resp2 = self.client.post(r('core:confirm_update'), data)

    def test_status_code(self):
        self.assertEqual(self.resp.status_code , 200)
        self.assertEqual(self.resp2.status_code , 200)
  
    def test_template_used(self):
        self.assertTemplateUsed(self.resp, 'atualizar.html')
    
    def test_data_changed(self):
        instance = AgendaModel.objects.first()
        self.assertEqual(instance.nome, 'MARIA JOSÉ')
        self.assertEqual(instance.telefone, '19666667777')


class Confirm_Update_POST_Fail_Test(TestCase):
    def setUp(self):
        data = {'nome': 'José da Silva',
                'telefone': '1988887777',}
        AgendaModel.objects.create(**data)
        data = {'telefone': '19666667777','id':1}
        self.resp = self.client.post(r('core:confirm_update'), data, follow=True)
        self.resp2 = self.client.post(r('core:confirm_update'), data)

    def test_status_code(self):
        self.assertEqual(self.resp.status_code , 200)
        self.assertEqual(self.resp2.status_code , 200)
  
    def test_template_used(self):
        self.assertTemplateUsed(self.resp, 'atualizar2.html')
    
    def test_data_not_changed(self):
        instance = AgendaModel.objects.first()
        self.assertEqual(instance.nome, 'José da Silva')
        self.assertEqual(instance.telefone, '1988887777')


class Confirm_Update_POST_Fail_2_Test(TestCase):
    def setUp(self):
        data = {'nome': 'José da Silva',
                'telefone': '1988887777',}
        AgendaModel.objects.create(**data)
        data = {'nome': 'José da Silva','telefone': '19666667777','id':2}
        self.resp = self.client.post(r('core:confirm_update'), data, follow=True)
        self.resp2 = self.client.post(r('core:confirm_update'), data)

    def test_status_code(self):
        self.assertEqual(self.resp.status_code , 404)
        self.assertEqual(self.resp2.status_code , 404)
  
    def test_data_not_changed(self):
        instance = AgendaModel.objects.first()
        self.assertEqual(instance.nome, 'José da Silva')
        self.assertEqual(instance.telefone, '1988887777')


class Delete_GET_Test(TestCase):
    def setUp(self):
        self.resp = self.client.get(r('core:delete'), follow=True)

    def test_status_code(self):
        self.assertEqual(self.resp.status_code , 200)
          
    def test_template_used(self):
        self.assertTemplateUsed(self.resp, 'remover.html')


class Delete_POST_OK_Test(TestCase):
    def setUp(self):
        data = {'nome': 'José da Silva',
                'telefone': '1988887777',}
        AgendaModel.objects.create(**data)
        data = {'id':1}
        self.resp = self.client.post(r('core:delete'), data, follow=True)

    def test_status_code(self):
        self.assertEqual(self.resp.status_code , 200)
  
    def test_template_used(self):
        self.assertTemplateUsed(self.resp, 'index.html')
    
    def test_deleted(self):
        self.assertFalse(AgendaModel.objects.exists())

class Delete_POST_Fail_Test(TestCase):
    def setUp(self):
        data = {'nome': 'José da Silva',
                'telefone': '1988887777',}
        AgendaModel.objects.create(**data)
        data = {'id':2}
        self.resp = self.client.post(r('core:delete'), data, follow=True)

    def test_status_code(self):
        self.assertEqual(self.resp.status_code , 200)
  
    def test_template_used(self):
        self.assertTemplateUsed(self.resp, 'index.html')
    
    def test_not_deleted(self):
        self.assertTrue(AgendaModel.objects.exists())
