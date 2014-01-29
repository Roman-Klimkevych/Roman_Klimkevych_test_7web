from notes.models import Notes

def total_count(request):
    """ 
    Create context variable "count" to show total count of text notes
    at every template.

    """
    count = Notes.objects.count()
    return {
            'count': count,
        }
