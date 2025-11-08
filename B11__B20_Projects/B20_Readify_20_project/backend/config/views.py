from django.http import FileResponse, Http404
from django.views.static import serve
import os
import logging
from django.conf import settings

logger = logging.getLogger(__name__)


def serve_media_file(request, path):
    media_root = settings.MEDIA_ROOT
    file_path = os.path.join(media_root, path)

    if not os.path.exists(file_path):
        raise Http404("File not found")

    try:
        if file_path.lower().endswith('.txt'):
            import chardet

            with open(file_path, 'rb') as f:
                raw_content = f.read()
                encoding_info = chardet.detect(raw_content)
                encoding = encoding_info.get('encoding', 'utf-8')

            with open(file_path, 'r', encoding=encoding, errors='replace') as f:
                content = f.read()

            from django.http import HttpResponse
            response = HttpResponse(content, content_type='text/plain; charset=utf-8')
            response['Content-Disposition'] = f'inline; filename="{os.path.basename(file_path)}"'
            return response

        else:
            return serve(request, path, document_root=media_root)

    except Exception as e:
        logger.error(f"Error serving media file {file_path}: {e}")
        raise Http404("Error reading file")