from supabase import create_client, Client

# Configure Supabase credentials here
SUPABASE_URL = None  # Set Supabase URL here
SUPABASE_KEY = None  # Set Supabase key here
SUPABASE_BUCKET = None  # Set Supabase bucket name here

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def upload_pdf_to_bucket(file_path: str, dest_filename: str) -> str:
    """
    Uploads a PDF file to the Supabase storage bucket and returns the public URL.
    """
    try:
        with open(file_path, "rb") as f:
            # The upload method returns an object or raises an exception if it fails
            supabase.storage.from_(SUPABASE_BUCKET).upload(
                dest_filename, 
                f, 
                file_options={"content-type": "application/pdf"},
            )
        
        # If we reached here, the upload was successful
        # Get public URL
        public_url = supabase.storage.from_(SUPABASE_BUCKET).get_public_url(dest_filename)
        return public_url
    except Exception as e:
        print(f"Upload error details: {str(e)}")
        raise

def insert_resume_record(resume_link: str, user_id: str):
    """
    Inserts a new record into the resume_table with the given resume_link and user_id.
    """
    from datetime import datetime
    import uuid
    data = {
        "id": str(uuid.uuid4()),
        "created_at": datetime.utcnow().isoformat(),
        "resume_link": resume_link,
        "user_id": user_id
    }
    try:
        response = supabase.table("resume_table").insert(data).execute()
        return response
    except Exception as e:
        print(f"Insert error details: {str(e)}")
        raise

if __name__ == "__main__":
    # Example usage
    file_path = "latex_output/7d1f0007-63e1-4e1a-b22b-54c4d836d628.pdf"  # Path to your PDF file
    dest_filename = f"{file_path}"  # Destination filename in the bucket
    try:
        public_url = upload_pdf_to_bucket(file_path, dest_filename)
        print(f"PDF uploaded successfully! Public URL: {public_url}")
    except Exception as e:
        print(f"Error uploading PDF: {str(e)}")