(function () {
    'use strict'
    // for image uploads
    FilePond.registerPlugin(
        FilePondPluginImagePreview,
        FilePondPluginImageExifOrientation,
        FilePondPluginFileValidateSize,
        FilePondPluginFileEncode,
        FilePondPluginImageEdit,
        FilePondPluginFileValidateType,
        FilePondPluginImageCrop,
        FilePondPluginImageResize,
        FilePondPluginImageTransform
    );
    
  const MultipleElement = document.querySelector('.multiple-filepond');
  FilePond.create(MultipleElement);

    /* Start::Choices JS */
    document.addEventListener('DOMContentLoaded', function () {
        var genericExamples = document.querySelectorAll('.product-tags');
        for (let i = 0; i < genericExamples.length; ++i) {
            var element = genericExamples[i];
            new Choices(element, {
                allowHTML: true,
                paste: false,
                duplicateItemsAllowed: false,
                editItems: true, 
                removeItemButton: true,
            });
        }
    }); 
    /* Start::Choices JS */
    document.addEventListener('DOMContentLoaded', function () {
        var genericExamples = document.querySelectorAll('.product-search');
        for (let i = 0; i < genericExamples.length; ++i) {
            var element = genericExamples[i];
            new Choices(element, {
                allowHTML: true,
                searchEnabled: false,
                removeItemButton: true,
            });
        }
    }); 

     //To choose date and time
    flatpickr("#product-datetime", {
        enableTime: true,
        dateFormat: "Y-m-d H:i",
    });

})();