// import secret_key;
// var mapbox_api_key = secret_key.mapbox_api_key;


describe("Render correct basemap", function() {

  it("The 'style' is the basemap", function() {
    var style = 'mapbox://styles/mapbox/light-v9';

    expect(style).toBe('mapbox://styles/mapbox/light-v9');
    expect(style).not.toBe(null);
  });
});

describe("Months contain correct months", function() {
    it("confirms correct months", function() {
        var months = [
            'January',
            'February',
            'March',
            'April',
            'May',
            'June',
            'July',
            'August',
            'September',
            'October',
            'November',
            'December'
        ];

      expect(months).toContain('October');
      expect(months).toContain('January');
      expect(a).not.toContain('bird');
    });
});

describe("Correct coordinates", function() {
    it("Latitude is not longitude", function() {
        var latitude = 32;
        var longitude = -112;

        expect(longitude).toBeLessThan(latitude);
        expect(latitude).not.toBeLessThan(longitude);
    });
});