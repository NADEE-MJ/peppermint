<script lang="ts">
	import '@skeletonlabs/skeleton/themes/theme-crimson.css';
	import '@skeletonlabs/skeleton/styles/all.css';
	import '../app.postcss';
	import { Toast } from '@skeletonlabs/skeleton';
</script>

<svelte:head>
	<title>peppermint</title>
	<meta name="description" content="peppermint finance tracker" />
</svelte:head>

<Toast position="t" />
<slot />
