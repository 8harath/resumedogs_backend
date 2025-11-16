from supabase import create_client, Client
from fastapi import HTTPException, status

# Configure Supabase credentials here
SUPABASE_URL = None  # Set Supabase URL here
SUPABASE_KEY = None  # Set Supabase key here
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def check_user_usage_limits(user_id: str):
    try:
        usage_data = (
            supabase.table("user_usage")
            .select("daily_conversions", "monthly_conversions")
            .eq("user_id", user_id)
            .maybe_single()
            .execute()
        )
        # Handle None result
        data = (usage_data.data if usage_data is not None else {}) or {}
        daily = data.get("daily_conversions", 0)
        monthly = data.get("monthly_conversions", 0)
        if daily >= 3:
            raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Daily conversion limit reached.")
        if monthly >= 30:
            raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Monthly conversion limit reached.")
        return daily, monthly
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Usage check failed: {str(e)}")

def increment_user_usage(user_id: str, daily: int, monthly: int):
    try:
        new_daily = daily + 1
        new_monthly = monthly + 1
        supabase.table("user_usage").update({
            "daily_conversions": new_daily,
            "monthly_conversions": new_monthly
        }).eq("user_id", user_id).execute()
    except Exception as e:
        # Log but don't block response
        print(f"Failed to increment usage counters: {e}")
