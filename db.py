import os
from supabase import create_client, Client

url = "https://ylyqbmswwnqzvomuoobf.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InlseXFibXN3d25xenZvbXVvb2JmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTM3Mjc2NDksImV4cCI6MjA2OTMwMzY0OX0.nfw2SHwxJ5_EnrMiOZVypGSdM7h0Gn2cvXS1Wp6rOqQ"
supabase: Client = create_client(url, key)