class BuddySystem:
    def __init__(self, total_memory):
        """
        Initialize the buddy system with total memory size.

        Parameters:
        total_memory (int): Total memory size (must be a power of 2).
        """
        if total_memory & (total_memory - 1) != 0:
            raise ValueError("Total memory size must be a power of 2.")

        self.total_memory = total_memory
        self.free_list = {total_memory: [0]}  # A dictionary storing free blocks by size
        self.allocated = {}  # Tracks allocated memory blocks and their sizes

    def next_power_of_two(self, size):
        """
        Calculate the next power of 2 greater than or equal to the given size.

        Parameters:
        size (int): The size to round up.

        Returns:
        int: The next power of 2.
        """
        if size & (size - 1) == 0:
            return size
        power = 1
        while power < size:
            power *= 2
        return power

    def allocate(self, size):
        """
        Allocate memory of a specified size using the buddy system algorithm.

        Parameters:
        size (int): Size of memory to allocate (rounded up to the next power of 2).

        Returns:
        int: Address of the allocated memory block.

        Raises:
        ValueError: If allocation fails.
        """
        size = self.next_power_of_two(size)

        if size > self.total_memory:
            raise ValueError("Requested size exceeds total memory.")

        # Find the smallest block that can satisfy the request
        for block_size in sorted(self.free_list):
            if block_size >= size and self.free_list[block_size]:
                address = self.free_list[block_size].pop(0)  # Remove the block from the free list

                # Split blocks until the desired size is reached
                while block_size > size:
                    block_size //= 2
                    buddy_address = address + block_size
                    self.free_list.setdefault(block_size, []).append(buddy_address)

                self.allocated[address] = size  # Track the allocated block
                return address

        raise ValueError("No suitable block available for allocation.")

    def free(self, address, size):
        """
        Free a previously allocated memory block.

        Parameters:
        address (int): Address of the block to free.
        size (int): Size of the block to free (must be a power of 2).

        Raises:
        ValueError: If invalid free operation is detected.
        """
        size = self.next_power_of_two(size)

        if size > self.total_memory:
            raise ValueError("Block size exceeds total memory.")

        if address not in self.allocated or self.allocated[address] != size:
            raise ValueError("Invalid free operation. Address and size do not match.")

        del self.allocated[address]  # Remove from allocated tracking

        # Merge free blocks (buddies) if possible
        while size < self.total_memory:
            buddy_address = address ^ size
            if buddy_address in self.free_list.get(size, []):
                self.free_list[size].remove(buddy_address)
                address = min(address, buddy_address)
                size *= 2
            else:
                break

        self.free_list.setdefault(size, []).append(address)
        self.free_list[size].sort()  # Optional: keep the free list sorted for readability

    def display_memory(self):
        """
        Display a detailed memory state including allocated and free blocks.
        """
        print("\nMemory Details:")
        print(f"Total Memory: {self.total_memory}KB")

        # Display allocated memory
        print("Allocated Memory:")
        if self.allocated:
            for address, size in sorted(self.allocated.items()):
                print(f"  Address: {address}KB, Block Size: {size}KB, Allocated: True")
        else:
            print("  No allocated memory blocks.")

        # Display free blocks
        print("Free Blocks:")
        for size in sorted(self.free_list, reverse=True):
            for address in self.free_list[size]:
                print(f"  Address: {address}KB, Block Size: {size}KB, Allocated: False")

    def display_blocks_by_size(self):
        """
        Display the state of blocks for specific sizes based on user input.
        """
        sizes = [512, 256, 128]  # Predefined block sizes
        print("\nBlocks by Size:")
        for size in sizes:
            print(f"Block Size: {size}KB")
            allocated = [addr for addr, s in self.allocated.items() if s == size]
            free = self.free_list.get(size, [])

            for address in allocated:
                print(f"  Address: {address}KB, Allocated: True")

            for address in free:
                print(f"  Address: {address}KB, Allocated: False")

    def __str__(self):
        """
        Return a string representation of the current memory state.
        """
        total_allocated = sum(self.allocated.values())
        total_free = self.total_memory - total_allocated

        state = []
        state.append(f"Total Memory: {self.total_memory}KB")
        state.append(f"Allocated Memory: {total_allocated}KB")
        state.append(f"Free Memory: {total_free}KB")
        state.append("Free Blocks:")

        for size in sorted(self.free_list, reverse=True):
            for address in self.free_list[size]:
                state.append(f"Block Size: {size}KB, Allocated: false")

        for address, size in sorted(self.allocated.items()):
            state.append(f"Block Size: {size}KB, Allocated: true")

        return "\n".join(state)

# Interactive menu for the Buddy System
if __name__ == "__main__":
    total_memory = 1024  # Initialize buddy system with 1024 units of memory
    buddy = BuddySystem(total_memory)

    while True:
        print("\nChoose an option:")
        print("1. Allocate Memory")
        print("2. Free Memory")
        print("3. Print Memory State")
        print("4. Display Blocks by Size")
        print("5. Exit")

        try:
            choice = int(input("Enter your choice: "))

            if choice == 1:
                try:
                    size = int(input("Enter memory size to allocate (in KB): "))
                    address = buddy.allocate(size)
                    print(f"Allocated block of size: {buddy.next_power_of_two(size)}KB at address {address}KB.")
                except ValueError as e:
                    print(f"Error: {e}")

            elif choice == 2:
                try:
                    address = int(input("Enter memory address to free: "))
                    size = int(input("Enter memory size to free (in KB): "))
                    buddy.free(address, size)
                    print(f"Freed {size}KB from address {address}KB.")
                except ValueError as e:
                    print(f"Error: {e}")

            elif choice == 3:
                print("\n", buddy)

            elif choice == 4:
                buddy.display_blocks_by_size()

            elif choice == 5:
                print("Exiting...")
                break

            else:
                print("Invalid choice. Please enter a number between 1 and 5.")

        except ValueError:
            print("Invalid input. Please enter a number.")
