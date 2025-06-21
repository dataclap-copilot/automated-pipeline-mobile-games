import hashlib
import bsdiff4
from google.cloud import storage

def generate_delta(old_version, new_version, platform):
    """Generate binary patch between versions"""
    client = storage.Client()
    bucket = client.bucket('game-assets')
    
    # Download builds
    old_blob = bucket.blob(f'builds/{platform}/{old_version}.apk')
    new_blob = bucket.blob(f'builds/{platform}/{new_version}.apk')
    
    old_data = old_blob.download_as_bytes()
    new_data = new_blob.download_as_bytes()
    
    # Generate delta
    delta = bsdiff4.diff(old_data, new_data)
    
    # Upload patch
    patch_name = f'patches/{platform}/{old_version}-{new_version}.delta'
    patch_blob = bucket.blob(patch_name)
    patch_blob.upload_from_string(delta)
    
    # Return patch metadata
    return {
        'size': len(delta),
        'hash': hashlib.sha256(delta).hexdigest(),
        'url': f'gs://game-assets/{patch_name}'
    }