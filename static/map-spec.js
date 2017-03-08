import secret_key
var mapbox_api_key = secret_key.mapbox_api_key

describe("My Test Suite", function () {

    it("should add numbers", function () {
        var sum = renderMap(mapbox_api_key, -121.8595805, 36.2819875, );
        expect(sum).toBe(5);
    });

    it("should add negative numbers", function () {
        expect(adder(1, -1)).toBe(99);
    });

});