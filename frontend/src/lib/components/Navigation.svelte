<script lang="ts">
    import { drawerStore } from "@skeletonlabs/skeleton";

    function drawerClose(): void {
        drawerStore.close();
    }
</script>

<nav class='list-nav p-4'>
    <ul>
        <li><a href="/client/skelly" on:click={drawerClose}>Skelly</a></li>
        <li><a href="https://github.com/NADEE-MJ/peppermint" on:click={drawerClose}>GitHub</a></li>
    </ul>
</nav>