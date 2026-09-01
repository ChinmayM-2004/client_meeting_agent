from memory.memory_store import search_memory


def memory_search(query, k=5):
    """
    Search long-term memory for information
    relevant to the user's query.
    """

    return search_memory(
        query,
        k=k
    )


# --------------------------------------------------
# Test
# --------------------------------------------------

if __name__ == "__main__":

    results = memory_search(
        "What do I know about Acme?"
    )

    if not results:

        print("No memories found.")

    else:

        for i, result in enumerate(
            results,
            start=1
        ):

            print(f"\n{'=' * 70}")
            print(f"Memory {i}")
            print(
                f"Type: {result['memory_type']}"
            )
            print(
                f"Distance: {result['distance']:.4f}"
            )
            print(
                f"Text: {result['text']}"
            )
