import marimo

__generated_with = "0.14.17"
app = marimo.App(width="medium")


@app.cell
async def _():
    import marimo as mo
    import micropip
    await micropip.install("ch35t==0.1.9")
    return (mo,)


@app.cell
def _():
    from ch35t import Chest
    return (Chest,)


@app.cell
def _(Chest, mo):
    def show_hint(chest):
        return mo.md(f"""
    # {chest.name()}

    {chest.hint}
    """)

    def load_chest(url: str):
        try:
            c = Chest(url.value, chests_dir="./chests")
            c.validate()
            return c, show_hint(c)
        except Exception as e:
            return None, mo.md(f"""# ERROR

            I could not load the URL: {url.value}. Perhaps it is not available yet?
            """)

    def unlock_chest(chest, pw):
        if not chest or not pw.value:
            return None

        if (chest.unlock(pw.value)):
            message = chest.payload.cleartext_data
            if not message:
                message = "There is no hidden content here so... Congratulations :-)"

            return mo.md(f"""# Password OK!

            {message}
            """)
        else:
            return mo.md("The password is wrong: the ch35t is still locked.")

    def password_field(chest):
        if not chest:
            return None

        return mo.ui.text(
            label="PASSWORD:",
            full_width=True,
            value="")

    url = mo.ui.text(
        label="URL",
        full_width=True,
        value="http://3564020356.org/ch35t/examples/deserve_b64.json")
    return load_chest, password_field, unlock_chest, url


@app.cell
def _(url):
    url
    return


@app.cell
def _(load_chest, url):
    c, md = load_chest(url)
    md
    return (c,)


@app.cell
def _(c, password_field):
    pw = password_field(c)
    pw
    return (pw,)


@app.cell
def _(c, pw, unlock_chest):
    unlock_chest(c, pw)
    return


if __name__ == "__main__":
    app.run()
