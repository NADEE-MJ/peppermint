<script lang="ts">
	import '@skeletonlabs/skeleton/themes/theme-crimson.css';
	import '@skeletonlabs/skeleton/styles/all.css';
	import '../app.postcss';
	import { Toast } from '@skeletonlabs/skeleton';
</script>

<svelte:head>
	<title>Peppermint</title>
	<meta name="description" content="Peppermint Finance Tracker" />
</svelte:head>

<Toast position="t" />
<slot />
