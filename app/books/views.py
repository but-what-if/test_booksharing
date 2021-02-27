import csv
import xlwt

from books.models import Book, Author, Log
from books.forms import BookForm, AuthorForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, TemplateView, View
from django.http import HttpResponse
from books.utils import display
# from pdb import set_trace; set_trace()


class FormUserKwargMixin:
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class Index(TemplateView):
    template_name = 'index.html'


class BookCreate(FormUserKwargMixin, CreateView):
    model = Book
    success_url = reverse_lazy('books:my-books')
    form_class = BookForm


class BookList(ListView):
    queryset = Book.objects.all().select_related('author')


class MyBooksList(LoginRequiredMixin, ListView):
    queryset = Book.objects.all().select_related('author')
    template_name = 'books/my_books.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)


class BookUpdate(FormUserKwargMixin, UpdateView):
    model = Book
    success_url = reverse_lazy('books:my-books')
    form_class = BookForm


class BookDelete(DeleteView):
    model = Book
    success_url = reverse_lazy('books:list')


class AuthorCreate(CreateView):
    model = Author
    success_url = reverse_lazy('authors-list')
    form_class = AuthorForm


class AuthorList(ListView):
    queryset = Author.objects.all()


class AuthorUpdate(UpdateView):
    model = Author
    success_url = reverse_lazy('authors-list')
    form_class = AuthorForm


class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('authors-list')


class LogList(ListView):
    queryset = Log.objects.all()


class DownloadCSVBookView(View):

    HEADERS = (
        'id',
        'title',
        'author.full_name',
        'author.get_full_name',
        'publish_year',
        'condition',
    )

    def get(self, request):
        # Create the HttpResponse object with the appropriate CSV header.
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'

        writer = csv.writer(response)

        writer.writerow(self.HEADERS)

        for book in Book.objects.all().select_related('author').iterator():
            writer.writerow([
                display(book, header)
                for header in self.HEADERS
            ])

        return response


class DownloadXLSXBookView(View):

    HEADERS = (
        'id',
        'title',
        'author.full_name',
        'author.get_full_name',
        'publish_year',
        'condition',
    )

    def download_excel_data(self, request):
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="ThePythonDjango.xls"'

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet("sheet1")

        row_num = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        for col_num in range(len(self.HEADERS)):
            ws.write(row_num, col_num, self.HEADERS[col_num], font_style)

        font_style = xlwt.XFStyle()

        for book in Book.objects.all().select_related('author').iterator():
            row_num = row_num + 1
            for col_num in range(len(self.HEADERS)):
                ws.write(row_num, col_num, book[self.HEADERS[col_num]], font_style)

        wb.save(response)
        return response
