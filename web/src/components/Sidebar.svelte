<script>
  import Button from "./Button.svelte";

  export let currentlyActiveScreen = "now_playing";

  export let onSidebarButtonClick = () => {};

  const handleSidebarButtonClick = (id) => {
    if (currentlyActiveScreen != id) currentlyActiveScreen = id;
    onSidebarButtonClick(id);
  };

  const toggleTheme = () => {
    window.document.body.classList.toggle("dark-mode");
  };
</script>

<div class="sidebar">
  <li class="sidebar-list">
    <Button
      textAlign="left"
      icon="play"
      label={"Now Playing"}
      onClick={() => handleSidebarButtonClick("now_playing")}
      isActive={currentlyActiveScreen == "now_playing"}
    />
    <Button
      textAlign="left"
      icon="search"
      label={"Search"}
      onClick={() => handleSidebarButtonClick("search")}
      isActive={currentlyActiveScreen == "search"}
    />

    <p class="sidebar-divider">Music</p>
    <Button
      textAlign="left"
      icon="bars"
      label={"Playlists"}
      onClick={() => handleSidebarButtonClick("playlists")}
      isActive={currentlyActiveScreen == "playlists"}
    />
    <Button
      textAlign="left"
      icon="users"
      label={"Artists"}
      onClick={() => handleSidebarButtonClick("artists")}
      isActive={currentlyActiveScreen == "artists"}
    />
    <Button
      textAlign="left"
      icon="record-vinyl"
      label={"Albums"}
      onClick={() => handleSidebarButtonClick("albums")}
      isActive={currentlyActiveScreen == "albums"}
    />
    <Button
      textAlign="left"
      icon="headphones"
      label={"Tracks"}
      onClick={() => handleSidebarButtonClick("tracks")}
      isActive={currentlyActiveScreen == "tracks"}
    />
    <Button textAlign="left" icon="sun" label={""} onClick={toggleTheme} />
  </li>
</div>

<style>
  .sidebar {
    background: #f4f2f0;
    height: calc(100vh - 66px);
    padding: 1rem;
    min-width: 5%;
    max-width: 20%;
    /* width: 100%; */
    border-right: 2px solid #eee !important;
    /* transition: 1s; */
  }

  .sidebar-list {
    list-style: none;
  }

  .sidebar-divider {
    font-family: Nunito;
    margin-top: 1rem;
    padding: 10px;
    /* font-size: 0.8rem; */
    font-weight: normal;
    color: #bbb;
  }

  :global(body.dark-mode) .sidebar {
    background: #050505;
    border-right: none !important;
  }
</style>
