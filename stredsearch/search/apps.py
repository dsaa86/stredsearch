from django.apps import AppConfig


class SearchConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "search"

    def ready(self):
        import search.signals
        from .signals import commit_questions_to_local_db_signal

        commit_questions_to_local_db_signal.connect(search.signals.commitNewQuestion)
