<script>
  export let label;
  export let background = "none";
  export let width = "100%";
  export let textAlign = "center";
  export let icon;
  export let isActive = false;
  export let activeBackground = "#08d58f";
  export let onClick = () => {};
</script>

<button
  on:click={onClick}
  style={`background: ${
    isActive ? activeBackground : background
  }; width: ${width}; text-align: ${textAlign};`}
  class={`button ${isActive && "active-sidebar-button"}`}
  ><i class={`fa fa-${icon}`} /><span class="button-label">{label}</span
  ></button
>

<style>
  .button {
    padding: 10px;
    border-radius: 5px;
    border: none;
    cursor: pointer;
    font-size: medium;
    font-weight: bold;
    font-family: Nunito;
  }

  .button > i {
    width: 1.75rem;
    font-size: 0.8rem;
  }

  .active-sidebar-button {
    color: white !important;
  }

  :global(body.dark-mode) .button {
    color: white;
  }
</style>
