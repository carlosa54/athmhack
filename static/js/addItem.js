$("#addItemButton").click(function() {
    var item = $("#items").val();
    var itemName = $("#items option:selected").text();
    var itemQuantity = $("#quantity").val();

    $("#itemsAdded").append("<tr><td>" + item + "</td>" +
                            "<td>" + itemName + "</td>" +
                            "<td>" + itemQuantity + "</td></tr>")
    $("#itemsAdded").append('<input name="id_' + item + '" type="hidden" value="' + item + '" />');
    $("#itemsAdded").append('<input name="name_' + item + '" type="hidden" value="' + itemName + '" />');
    $("#itemsAdded").append('<input name="quantity_' + item + '" type="hidden" value="' + itemQuantity + '" />');
});