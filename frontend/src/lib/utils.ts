import { toast } from './toasts';

export const uploadFile = async (file: File, mapping: object, URL: string) => {
	if (!mapping) {
		toast.error('Please enter a mapping');
		return false;
	}

	const headers = { 'Content-Type': 'application/json' };
	const body = JSON.stringify({ file: await fileToBase64(file), mapping });
	const res = await fetch(URL, { method: 'POST', body, headers });
	const result = await res.json();

	result?.success ? toast.success('File uploaded successfully ✅') : toast.error('File upload failed ❌');
	return true;
};

export const fileToBase64 = (file: File): Promise<string | null> => {
	return new Promise((resolve, reject) => {
		const reader = new FileReader();
		reader.readAsBinaryString(file);

		reader.onload = () => {
			const result = reader.result;
			if (typeof result === 'string') {
				const base64data = window.btoa(result);
				const mimeType = file.type;

				resolve(`Data:${mimeType};base64,${base64data}`);
			}
		};

		reader.onerror = (error) => {
			toast.error(`Error converting file to base64: ${error}`);
			reject(null);
		};
	});
};
