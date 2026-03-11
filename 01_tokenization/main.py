import tiktoken

enc = tiktoken.encoding_for_model("gpt-4o")

txt = "How is the weather in amritsar?"

tokens = enc.encode(txt)

print("tokens", tokens)

# tokens = [5299, 382, 290, 11122, 306, 939, 1166, 103241, 30]

decoded = enc.decode([5299, 382, 290, 11122, 306, 939, 1166, 103241, 30])

print("decoded-:", decoded)