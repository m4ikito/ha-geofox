# HVV Transport Integration for Home Assistant

This custom integration allows you to access public transport information from the HVV (Hamburger Verkehrsverbund) via the Geofox API in Home Assistant.

## Features

- Retrieve information about stops and departures.
- Get route information between two stops.
- Display departure times and route details in your Home Assistant dashboard.

## Installation

### Using HACS

1. Open HACS in your Home Assistant interface.
2. Go to "Integrations" and click the "+" button to add a new integration.
3. Enter the following repository URL: `https://github.com/m4ikito/ha-geofox`.
4. Choose the "Integration" category.
5. Install the integration.

### Manual Installation

1. Clone this repository or download it as a ZIP file.
2. Place the `hvv_transport` folder in your `custom_components` directory in your Home Assistant configuration directory.

## Configuration

To set up the integration, add the following configuration to your `configuration.yaml`:

```yaml
hvv_transport:
  username: YOUR_USERNAME
  password: YOUR_PASSWORD
