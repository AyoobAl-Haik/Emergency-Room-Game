from game_manager import GameManager

def main():
    game = GameManager(num_bays=3)
    
    while True:
        print(f"\n--- TURN {game.turn} ---")
        game.process_turn()

        # Print waiting list
        print("\nWaiting List:")
        if game.waiting_list:
            for i, p in enumerate(game.waiting_list):
                print(f"{i}: {p}")
        else:
            print("(empty)")

        # Print bays
        print("\nBays:")
        for i, p in enumerate(game.bays.get_patients()):
            print(f"Bay {i}: {p}")

        # Code status check
        codes = game.coded_patients()
        if codes:
            print("\n🚨 CODE BLUE patients:")
            for c in codes:
                print(c)

        # Player action
        print("\nActions:")
        print("1. Move patient from waiting list to bay")
        print("2. Apply treatment to bay patient")
        print("3. End turn")

        choice = input("Choose: ")

        if choice == "1":
            if not game.waiting_list:
                print("No patients in waiting list.")
                continue
            idx_w = int(input("Waiting index: "))
            if idx_w < 0 or idx_w >= len(game.waiting_list):
                print("Invalid waiting list index.")
                continue
            idx_b = int(input("Bay index: "))
            p = game.waiting_list.pop(idx_w)
            if not game.bays.assign_patient(p, idx_b):
                print("Bay occupied.")
                game.waiting_list.append(p)

        elif choice == "2":
            idx_b = int(input("Bay index: "))
            tx = input("Treatment name (fluids/antibiotics/transfusion/hemostasis/cpr/defibrillation): ")
            result = game.apply_treatment(idx_b, tx)
            if result:
                print(result)

        elif choice == "3":
            continue

if __name__ == "__main__":
    main()
