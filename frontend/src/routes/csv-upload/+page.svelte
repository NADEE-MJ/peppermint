<script lang="ts">
    import { FileButton, FileDropzone } from "@skeletonlabs/skeleton"
    
    let files: FileList;
    
    // function onChangeHandler(e: any) {
    //     console.log('files', e)
    //     console.log('file data', files[0].toString, files[0].stream)
    // }

    let currFile: File;

    async function onChangeHandler(e: any) {
            files = e.target.files;
            console.log("files", files);
            console.log("file name", files[0].name);
            console.log("file type", files[0].type);
            console.log("file size", files[0].size);
            console.log("files[0] typeof", typeof files[0]);
            console.log("files[0]", files[0]);
            console.log('test123', fileToBase64(files[0]))
            console.log('url', URL.createObjectURL(files[0]));
            console.log( await files[0].text())
            // You can also read the contents of the file using the FileReader API
            const reader = new FileReader();
            reader.readAsText(files[0]);
            reader.onload = function () {
            console.log(reader.result);
            currFile = files[0];
        };
    }
function uploadFile() {
  let data = new FormData()
  data.set('file', currFile);
  fetch('/csv-upload', {method: "POST", body: data })
}

function fileToBase64(file: File) {
  const reader = new FileReader();
  reader.readAsBinaryString(file);

  // Wait for the file to be loaded
  reader.onload = () => {
      const result = reader.result;
      if 
      // Convert the binary string to a base64 encoded string
      const base64data = btoa();

      // Get the file's mime type
      const mimeType = file.type;

      // Do something with the base64 encoded string and mime type
      return `Data:${mimeType};base64,${base64data}`;
  };
}

// async function onChangeHandler(e: any) {
//   const file = e.target.files[0];
//   const formData = new FormData();
//   formData.append('file', file);

//   try {
//     const response = await fetch('/uploadFile', {
//       method: 'POST',
//       body: formData
//     });

//     if (!response.ok) {
//       throw new Error('Failed to upload file');
//     }

//     const result = await response.json();
//     console.log(result);
//   } catch (error) {
//     console.error(error);
//   }
// }
</script>

<div class="form max-w-lg">
    <!-- <form method="post" action="?/uploadFile"> -->
        <!-- <FileDropzone name="file" bind:files on:change={onChangeHandler}/> -->
        <FileDropzone name="file" on:change={onChangeHandler}/>
        <!-- <button type="submit" class="btn mt-2 variant-filled">Upload</button> -->
        <button type="button" on:click={uploadFile} class="btn mt-2 variant-filled">Upload</button>
    <!-- </form> -->

</div>
