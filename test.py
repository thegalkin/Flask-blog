textContent = "Текст а вот и <script>delete whole site!!!!!</script>]"

for i in r"^%&<>\[\]{}]/":
    textContent = textContent.replace(i, "", -1)
print(textContent)    