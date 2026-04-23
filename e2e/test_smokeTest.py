from playwright.sync_api import Page, expect



nomePlaylist = "Playlist Massa do Teste"

def test_home(page: Page):
    page.goto("/")
    expect(page).to_have_title("FocusFluir")  # ou um texto da página



def test_playlist_criar (page: Page):
    page.goto("http://localhost:5000/")
    
    page.click("text=Criar Playlists")

    page.fill("input[name='nome_playlist']",nomePlaylist)

    page.fill("" \
        "textarea[name='links_musica']",
        "https://www.youtube.com/watch?v=a1vHjBy85TU&list=RDa1vHjBy85TU&start_radio=1 \n https://www.youtube.com/watch?v=wWvu34x2INc&list=RDwWvu34x2INc&start_radio=1"
    )

    page.click("button[type='submit']")

    expect(page.locator("text=" + nomePlaylist)).to_be_visible()

    item = page.locator(".playlist-list li").filter(has_text=nomePlaylist)
    item.get_by_role("link", name="❌").click()

    expect(page.locator("body")).not_to_contain_text(nomePlaylist)
