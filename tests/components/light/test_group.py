"""The tests for the Group Light platform."""
from unittest.mock import MagicMock

import asynctest

from homeassistant.components import light
from homeassistant.components.light import group
from homeassistant.setup import async_setup_component


async def test_default_state(hass):
    """Test light group default state."""
    await async_setup_component(hass, 'light', {'light': {
        'platform': 'group', 'entities': [], 'name': 'Bedroom Group'
    }})
    await hass.async_block_till_done()

    state = hass.states.get('light.bedroom_group')
    assert state is not None
    assert state.state == 'unavailable'
    assert state.attributes['supported_features'] == 0
    assert state.attributes.get('brightness') is None
    assert state.attributes.get('rgb_color') is None
    assert state.attributes.get('xy_color') is None
    assert state.attributes.get('color_temp') is None
    assert state.attributes.get('white_value') is None
    assert state.attributes.get('effect_list') is None
    assert state.attributes.get('effect') is None


async def test_state_reporting(hass):
    """Test the state reporting."""
    await async_setup_component(hass, 'light', {'light': {
        'platform': 'group', 'entities': ['light.test1', 'light.test2']
    }})

    hass.states.async_set('light.test1', 'on')
    hass.states.async_set('light.test2', 'unavailable')
    await hass.async_block_till_done()
    assert hass.states.get('light.group_light').state == 'on'

    hass.states.async_set('light.test1', 'on')
    hass.states.async_set('light.test2', 'off')
    await hass.async_block_till_done()
    assert hass.states.get('light.group_light').state == 'on'

    hass.states.async_set('light.test1', 'off')
    hass.states.async_set('light.test2', 'off')
    await hass.async_block_till_done()
    assert hass.states.get('light.group_light').state == 'off'

    hass.states.async_set('light.test1', 'unavailable')
    hass.states.async_set('light.test2', 'unavailable')
    await hass.async_block_till_done()
    assert hass.states.get('light.group_light').state == 'unavailable'


async def test_brightness(hass):
    """Test brightness reporting."""
    await async_setup_component(hass, 'light', {'light': {
        'platform': 'group', 'entities': ['light.test1', 'light.test2']
    }})

    hass.states.async_set('light.test1', 'on',
                          {'brightness': 255, 'supported_features': 1})
    await hass.async_block_till_done()
    state = hass.states.get('light.group_light')
    assert state.state == 'on'
    assert state.attributes['supported_features'] == 1
    assert state.attributes['brightness'] == 255

    hass.states.async_set('light.test2', 'on',
                          {'brightness': 100, 'supported_features': 1})
    await hass.async_block_till_done()
    state = hass.states.get('light.group_light')
    assert state.state == 'on'
    assert state.attributes['brightness'] == 177

    hass.states.async_set('light.test1', 'off',
                          {'brightness': 255, 'supported_features': 1})
    await hass.async_block_till_done()
    state = hass.states.get('light.group_light')
    assert state.state == 'on'
    assert state.attributes['supported_features'] == 1
    assert state.attributes['brightness'] == 100


async def test_xy_color(hass):
    """Test XY reporting."""
    await async_setup_component(hass, 'light', {'light': {
        'platform': 'group', 'entities': ['light.test1', 'light.test2']
    }})

    hass.states.async_set('light.test1', 'on',
                          {'xy_color': (1.0, 1.0), 'supported_features': 64})
    await hass.async_block_till_done()
    state = hass.states.get('light.group_light')
    assert state.state == 'on'
    assert state.attributes['supported_features'] == 64
    assert state.attributes['xy_color'] == (1.0, 1.0)

    hass.states.async_set('light.test2', 'on',
                          {'xy_color': (0.5, 0.5), 'supported_features': 64})
    await hass.async_block_till_done()
    state = hass.states.get('light.group_light')
    assert state.state == 'on'
    assert state.attributes['xy_color'] == (0.75, 0.75)

    hass.states.async_set('light.test1', 'off',
                          {'xy_color': (1.0, 1.0), 'supported_features': 64})
    await hass.async_block_till_done()
    state = hass.states.get('light.group_light')
    assert state.state == 'on'
    assert state.attributes['xy_color'] == (0.5, 0.5)


async def test_rgb_color(hass):
    """Test RGB reporting."""
    await async_setup_component(hass, 'light', {'light': {
        'platform': 'group', 'entities': ['light.test1', 'light.test2']
    }})

    hass.states.async_set('light.test1', 'on',
                          {'rgb_color': (255, 0, 0), 'supported_features': 16})
    await hass.async_block_till_done()
    state = hass.states.get('light.group_light')
    assert state.state == 'on'
    assert state.attributes['supported_features'] == 16
    assert state.attributes['rgb_color'] == (255, 0, 0)

    hass.states.async_set('light.test2', 'on',
                          {'rgb_color': (255, 255, 255),
                           'supported_features': 16})
    await hass.async_block_till_done()
    state = hass.states.get('light.group_light')
    assert state.attributes['rgb_color'] == (255, 127, 127)

    hass.states.async_set('light.test1', 'off',
                          {'rgb_color': (255, 0, 0), 'supported_features': 16})
    await hass.async_block_till_done()
    state = hass.states.get('light.group_light')
    assert state.attributes['rgb_color'] == (255, 255, 255)


async def test_white_value(hass):
    """Test white value reporting."""
    await async_setup_component(hass, 'light', {'light': {
        'platform': 'group', 'entities': ['light.test1', 'light.test2']
    }})

    hass.states.async_set('light.test1', 'on',
                          {'white_value': 255, 'supported_features': 128})
    await hass.async_block_till_done()
    state = hass.states.get('light.group_light')
    assert state.attributes['white_value'] == 255

    hass.states.async_set('light.test2', 'on',
                          {'white_value': 100, 'supported_features': 128})
    await hass.async_block_till_done()
    state = hass.states.get('light.group_light')
    assert state.attributes['white_value'] == 177

    hass.states.async_set('light.test1', 'off',
                          {'white_value': 255, 'supported_features': 128})
    await hass.async_block_till_done()
    state = hass.states.get('light.group_light')
    assert state.attributes['white_value'] == 100


async def test_color_temp(hass):
    """Test color temp reporting."""
    await async_setup_component(hass, 'light', {'light': {
        'platform': 'group', 'entities': ['light.test1', 'light.test2']
    }})

    hass.states.async_set('light.test1', 'on',
                          {'color_temp': 2, 'supported_features': 2})
    await hass.async_block_till_done()
    state = hass.states.get('light.group_light')
    assert state.attributes['color_temp'] == 2

    hass.states.async_set('light.test2', 'on',
                          {'color_temp': 1000, 'supported_features': 2})
    await hass.async_block_till_done()
    state = hass.states.get('light.group_light')
    assert state.attributes['color_temp'] == 501

    hass.states.async_set('light.test1', 'off',
                          {'color_temp': 2, 'supported_features': 2})
    await hass.async_block_till_done()
    state = hass.states.get('light.group_light')
    assert state.attributes['color_temp'] == 1000


async def test_min_max_mireds(hass):
    """Test min/max mireds reporting."""
    await async_setup_component(hass, 'light', {'light': {
        'platform': 'group', 'entities': ['light.test1', 'light.test2']
    }})

    hass.states.async_set('light.test1', 'on',
                          {'min_mireds': 2, 'max_mireds': 5,
                           'supported_features': 2})
    await hass.async_block_till_done()
    state = hass.states.get('light.group_light')
    assert state.attributes['min_mireds'] == 2
    assert state.attributes['max_mireds'] == 5

    hass.states.async_set('light.test2', 'on',
                          {'min_mireds': 7, 'max_mireds': 1234567890,
                           'supported_features': 2})
    await hass.async_block_till_done()
    state = hass.states.get('light.group_light')
    assert state.attributes['min_mireds'] == 2
    assert state.attributes['max_mireds'] == 1234567890

    hass.states.async_set('light.test1', 'off',
                          {'min_mireds': 1, 'max_mireds': 2,
                           'supported_features': 2})
    await hass.async_block_till_done()
    state = hass.states.get('light.group_light')
    assert state.attributes['min_mireds'] == 1
    assert state.attributes['max_mireds'] == 1234567890


async def test_effect_list(hass):
    """Test effect_list reporting."""
    await async_setup_component(hass, 'light', {'light': {
        'platform': 'group', 'entities': ['light.test1', 'light.test2']
    }})

    hass.states.async_set('light.test1', 'on',
                          {'effect_list': ['None', 'Random', 'Colorloop']})
    await hass.async_block_till_done()
    state = hass.states.get('light.group_light')
    assert set(state.attributes['effect_list']) == {
        'None', 'Random', 'Colorloop'}

    hass.states.async_set('light.test2', 'on',
                          {'effect_list': ['None', 'Random', 'Rainbow']})
    await hass.async_block_till_done()
    state = hass.states.get('light.group_light')
    assert set(state.attributes['effect_list']) == {
        'None', 'Random', 'Colorloop', 'Rainbow'}

    hass.states.async_set('light.test1', 'off',
                          {'effect_list': ['None', 'Colorloop', 'Seven']})
    await hass.async_block_till_done()
    state = hass.states.get('light.group_light')
    assert set(state.attributes['effect_list']) == {
        'None', 'Random', 'Colorloop', 'Seven', 'Rainbow'}


async def test_effect(hass):
    """Test effect reporting."""
    await async_setup_component(hass, 'light', {'light': {
        'platform': 'group', 'entities': ['light.test1', 'light.test2',
                                          'light.test3']
    }})

    hass.states.async_set('light.test1', 'on',
                          {'effect': 'None', 'supported_features': 2})
    await hass.async_block_till_done()
    state = hass.states.get('light.group_light')
    assert state.attributes['effect'] == 'None'

    hass.states.async_set('light.test2', 'on',
                          {'effect': 'None', 'supported_features': 2})
    await hass.async_block_till_done()
    state = hass.states.get('light.group_light')
    assert state.attributes['effect'] == 'None'

    hass.states.async_set('light.test3', 'on',
                          {'effect': 'Random', 'supported_features': 2})
    await hass.async_block_till_done()
    state = hass.states.get('light.group_light')
    assert state.attributes['effect'] == 'None'

    hass.states.async_set('light.test1', 'off',
                          {'effect': 'None', 'supported_features': 2})
    hass.states.async_set('light.test2', 'off',
                          {'effect': 'None', 'supported_features': 2})
    await hass.async_block_till_done()
    state = hass.states.get('light.group_light')
    assert state.attributes['effect'] == 'Random'


async def test_supported_features(hass):
    """Test supported features reporting."""
    await async_setup_component(hass, 'light', {'light': {
        'platform': 'group', 'entities': ['light.test1', 'light.test2']
    }})

    hass.states.async_set('light.test1', 'on',
                          {'supported_features': 0})
    await hass.async_block_till_done()
    state = hass.states.get('light.group_light')
    assert state.attributes['supported_features'] == 0

    hass.states.async_set('light.test2', 'on',
                          {'supported_features': 2})
    await hass.async_block_till_done()
    state = hass.states.get('light.group_light')
    assert state.attributes['supported_features'] == 2

    hass.states.async_set('light.test1', 'off',
                          {'supported_features': 41})
    await hass.async_block_till_done()
    state = hass.states.get('light.group_light')
    assert state.attributes['supported_features'] == 43

    hass.states.async_set('light.test2', 'off',
                          {'supported_features': 256})
    await hass.async_block_till_done()
    state = hass.states.get('light.group_light')
    assert state.attributes['supported_features'] == 41


async def test_service_calls(hass):
    """Test service calls."""
    await async_setup_component(hass, 'light', {'light': [
        {'platform': 'demo'},
        {'platform': 'group', 'entities': ['light.bed_light',
                                           'light.ceiling_lights',
                                           'light.kitchen_lights']}
    ]})
    await hass.async_block_till_done()
    await hass.async_block_till_done()

    assert hass.states.get('light.group_light').state == 'on'
    light.async_toggle(hass, 'light.group_light')
    await hass.async_block_till_done()
    await hass.async_block_till_done()

    assert hass.states.get('light.bed_light').state == 'off'
    assert hass.states.get('light.ceiling_lights').state == 'off'
    assert hass.states.get('light.kitchen_lights').state == 'off'

    light.async_turn_on(hass, 'light.group_light')
    await hass.async_block_till_done()
    await hass.async_block_till_done()

    assert hass.states.get('light.bed_light').state == 'on'
    assert hass.states.get('light.ceiling_lights').state == 'on'
    assert hass.states.get('light.kitchen_lights').state == 'on'

    light.async_turn_off(hass, 'light.group_light')
    await hass.async_block_till_done()
    await hass.async_block_till_done()

    assert hass.states.get('light.bed_light').state == 'off'
    assert hass.states.get('light.ceiling_lights').state == 'off'
    assert hass.states.get('light.kitchen_lights').state == 'off'

    light.async_turn_on(hass, 'light.group_light', brightness=128,
                        effect='Random', rgb_color=(42, 255, 255))
    await hass.async_block_till_done()
    await hass.async_block_till_done()

    state = hass.states.get('light.bed_light')
    assert state.state == 'on'
    assert state.attributes['brightness'] == 128
    assert state.attributes['effect'] == 'Random'
    assert state.attributes['rgb_color'] == (42, 255, 255)

    state = hass.states.get('light.ceiling_lights')
    assert state.state == 'on'
    assert state.attributes['brightness'] == 128
    assert state.attributes['effect'] == 'Random'
    assert state.attributes['rgb_color'] == (42, 255, 255)

    state = hass.states.get('light.kitchen_lights')
    assert state.state == 'on'
    assert state.attributes['brightness'] == 128
    assert state.attributes['effect'] == 'Random'
    assert state.attributes['rgb_color'] == (42, 255, 255)


async def test_invalid_service_calls(hass):
    """Test invalid service call arguments get discarded."""
    add_devices = MagicMock()
    await group.async_setup_platform(hass, {
        'entities': ['light.test1', 'light.test2']
    }, add_devices)

    assert add_devices.call_count == 1
    grouped_light = add_devices.call_args[0][0][0]
    grouped_light.hass = hass

    with asynctest.patch.object(hass.services, 'async_call') as mock_call:
        await grouped_light.async_turn_on(brightness=150, four_oh_four='404')
        data = {
            'entity_id': ['light.test1', 'light.test2'],
            'brightness': 150
        }
        mock_call.assert_called_once_with('light', 'turn_on', data,
                                          blocking=True)
        mock_call.reset_mock()

        await grouped_light.async_turn_off(transition=4, four_oh_four='404')
        data = {
            'entity_id': ['light.test1', 'light.test2'],
            'transition': 4
        }
        mock_call.assert_called_once_with('light', 'turn_off', data,
                                          blocking=True)
        mock_call.reset_mock()

        data = {
            'brightness': 150,
            'xy_color': (0.5, 0.42),
            'rgb_color': (80, 120, 50),
            'color_temp': 1234,
            'white_value': 1,
            'effect': 'Sunshine',
            'transition': 4,
            'flash': 'long'
        }
        await grouped_light.async_turn_on(**data)
        data['entity_id'] = ['light.test1', 'light.test2']
        mock_call.assert_called_once_with('light', 'turn_on', data,
                                          blocking=True)
