def score_targets(aps):
    if not aps:
        print("[!] No access points found.")
        return None

    # Calculate scores
    for ap in aps:
        # Power is a negative value, so we add 100 to make it a positive score contribution.
        # A stronger signal (e.g., -30) will result in a higher score than a weaker one (e.g., -80).
        power_score = 100 + ap.get('power', -100)
        client_score = ap.get('clients', 0) * 10
        ap['score'] = power_score + client_score

    # Sort by score
    sorted_aps = sorted(aps, key=lambda x: x['score'], reverse=True)

    print("[+] Available Access Points (sorted by score):")
    print("    #  ESSID                 BSSID               CH   PWR  CLIENTS  SCORE")
    print("    -  --------------------  -----------------   --   ---  -------  -----")
    for i, ap in enumerate(sorted_aps):
        essid = ap.get("ESSID", "<hidden>")[:20]
        bssid = ap.get("BSSID", "?")
        channel = ap.get("channel", "?")
        power = ap.get("power", "?")
        clients = ap.get("clients", "?")
        score = int(ap.get("score", 0))
        print(f"  {i: >3}. {essid: <20}  {bssid: <17}   {channel: >2}  {power: >4}  {clients: >7}  {score: >5}")

    try:
        default_choice = 0
        choice_str = input(f"[?] Select target number (default: {default_choice}): ")
        if not choice_str:
            choice = default_choice
        else:
            choice = int(choice_str)
        
        return sorted_aps[choice]
    except (ValueError, IndexError):
        print("[!] Invalid selection.")
        return None

