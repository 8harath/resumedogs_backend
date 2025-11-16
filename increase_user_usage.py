def increment_user_usage(user_id: str):
    """Increment daily and monthly conversions by 1 for a user."""
    # Fetch current counts with exception handling
    try:
        result = (
            supabase.table("user_usage")
            .select("daily_conversions", "monthly_conversions")
            .eq("user_id", user_id)
            .single()
            .execute()
        )
    except APIError as e:
        print(f"Error fetching usage for user {user_id}: {e}")
        return None
    data = result.data or {}
    new_daily = (data.get("daily_conversions") or 0) + 1
    new_monthly = (data.get("monthly_conversions") or 0) + 1
    # Update counts with exception handling
    try:
        update_res = (
            supabase.table("user_usage")
            .update({
                "daily_conversions": new_daily,
                "monthly_conversions": new_monthly
            })
            .eq("user_id", user_id)
            .execute()
        )
        return update_res
    except APIError as e:
        print(f"Error updating usage for user {user_id}: {e}")
        return None


if __name__ == "__main__":
    res = increment_user_usage(user_id)
    # print("User usage incremented successfully.")
    print(res)