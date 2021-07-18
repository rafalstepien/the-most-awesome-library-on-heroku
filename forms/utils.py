
class BookFilterer:
    """
    Class building filtering queries
    """
    def __init__(
            self,
            queryset,
            title,
            author,
            language,
            date_after,
            date_before):
        self.queryset = queryset
        self.title = title
        self.author = author
        self.language = language
        self.date_after = date_after
        self.date_before = date_before

    def build_queryset(self):
        self.filter_by_title()
        self.filter_by_author()
        self.filter_by_language()
        self.filter_by_publication_date()
        return self.queryset

    def filter_by_title(self):
        if self.title is not None:
            self.queryset = self.queryset.filter(
                title__icontains=f'{self.title}')

    def filter_by_author(self):
        if self.author is not None:
            self.queryset = self.queryset.filter(
                author__icontains=f'{self.author}')

    def filter_by_language(self):
        if self.language is not None:
            self.queryset = self.queryset.filter(
                language__icontains=f'{self.language}')

    def filter_by_publication_date(self):
        if self.date_after is not None and self.date_before is not None:
            self.queryset = self.queryset.filter(
                publication_date__range=[
                    self.date_after, self.date_before])

        elif self.date_after is not None:
            self.queryset = self.queryset.filter(
                publication_date__gte=self.date_after)

        elif self.date_before is not None:
            self.queryset = self.queryset.filter(
                publication_date__gte=self.date_before)


def get_clicked_button_id(request_post: dict) -> int:
    """Get the ID of clicked button

    Args:
        request_post (dict): Dictionary with request.POST info

    Returns:
        int: ID of button being clicked
    """
    full_button_name = [
        key for key in request_post if 'button_number_' in key][0]
    button_id = int(full_button_name.replace('button_number_', ''))
    return button_id


def delete_button_is_clicked(request_post):
    return [key for key in request_post if 'button_number_' in key]
