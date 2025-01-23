import pytest
from main import BooksCollector


class TestBooksCollector:

    def test_add_new_book_add_two_books(self):
        collector = BooksCollector()
        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Что делать, если ваш кот хочет вас убить')
        assert len(collector.get_books_genre()) == 2

    def test_set_book_genre_with_existing_book_and_valid_genre_updates_genre(self):
        collector = BooksCollector()
        collector.add_new_book('Оно')
        collector.set_book_genre('Оно', 'Ужасы')
        assert collector.get_book_genre('Оно') == 'Ужасы'

    def test_get_book_genre_for_existing_book_returns_correct_genre(self):
        collector = BooksCollector()
        collector.add_new_book('Метро 2033')
        collector.set_book_genre('Метро 2033', 'Ужасы')
        assert collector.get_book_genre('Метро 2033') == 'Ужасы'

    @pytest.mark.parametrize("genre,expected_books", [
        ('Фантастика', ['Дюна', 'Облачный атлас']),
        ('Ужасы', ['Оно', 'Дракула']),
        ('Комедии', []),
    ])
    def test_get_books_with_specific_genre_returns_books_matching_genre(self, genre, expected_books):
        collector = BooksCollector()
        collector.add_new_book('Дюна')
        collector.set_book_genre('Дюна', 'Фантастика')
        collector.add_new_book('Облачный атлас')
        collector.set_book_genre('Облачный атлас', 'Фантастика')
        collector.add_new_book('Оно')
        collector.set_book_genre('Оно', 'Ужасы')
        collector.add_new_book('Дракула')
        collector.set_book_genre('Дракула', 'Ужасы')

        assert collector.get_books_with_specific_genre(genre) == expected_books

    def test_get_books_genre_after_adding_books_returns_correct_genre_mapping(self):
        collector = BooksCollector()
        collector.add_new_book('Гордость и предубеждение')
        collector.set_book_genre('Гордость и предубеждение', 'Комедии')
        collector.add_new_book('Облачный атлас')
        collector.set_book_genre('Облачный атлас', 'Фантастика')
        assert collector.get_books_genre() == {
            'Гордость и предубеждение': 'Комедии',
            'Облачный атлас': 'Фантастика',
        }

    @pytest.mark.parametrize("books,expected_books_for_children", [
        (
                [('Дюна', 'Фантастика'), ('Оно', 'Ужасы')],
                ['Дюна'],
        ),
        (
                [('Человек-амфибия', 'Фантастика'), ('Шерлок Холмс', 'Детективы')],
                ['Человек-амфибия'],
        ),
        (
                [('Облачный атлас', 'Фантастика'), ('Оно', 'Ужасы')],
                ['Облачный атлас'],
        ),
    ])
    def test_get_books_for_children_returns_only_child_friendly_books(self, books, expected_books_for_children):
        collector = BooksCollector()
        for book, genre in books:
            collector.add_new_book(book)
            collector.set_book_genre(book, genre)

        assert collector.get_books_for_children() == expected_books_for_children

    def test_add_book_in_favorites_with_valid_book_adds_to_favorites(self):
        collector = BooksCollector()
        collector.add_new_book('Шерлок Холмс')
        collector.add_book_in_favorites('Шерлок Холмс')
        assert 'Шерлок Холмс' in collector.get_list_of_favorites_books()

    def test_delete_book_from_favorites_removes_book_from_favorites(self):
        collector = BooksCollector()
        collector.add_new_book('Шерлок Холмс')
        collector.add_book_in_favorites('Шерлок Холмс')
        collector.delete_book_from_favorites('Шерлок Холмс')
        assert 'Шерлок Холмс' not in collector.get_list_of_favorites_books()

    def test_get_list_of_favorites_books_returns_correct_list(self):
        collector = BooksCollector()
        collector.add_new_book('Дюна')
        collector.add_book_in_favorites('Дюна')
        assert collector.get_list_of_favorites_books() == ['Дюна']

    def test_add_new_book_with_invalid_name_does_not_add_book(self):
        collector = BooksCollector()
        collector.add_new_book('Я в своем познании настолько преисполнился')
        assert len(collector.get_books_genre()) == 0
