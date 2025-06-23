from jnius import PythonJavaClass, java_method


class PlayerListener(PythonJavaClass):
    __javainterfaces__ = ["androidx/media3/common/Player$Listener"]
    __javacontext__ = "app"

    def __init__(self, player):
        self.player = player

    def call_player_method(self, method_name, *args):
        if hasattr(self.player, method_name):
            getattr(self.player, method_name)(*args)

    @java_method("(Landroidx/media3/common/Player;Landroidx/media3/common/Player$Events;)V")
    def onEvents(self, player, events):
        self.call_player_method("on_events", player, events)

    @java_method("(Landroidx/media3/common/Timeline;I)V")
    def onTimelineChanged(self, timeline, reason):
        self.call_player_method("on_timeline_changed", timeline, reason)

    @java_method("(Landroidx/media3/common/MediaItem;I)V")
    def onMediaItemTransition(self, media_item, reason):
        self.call_player_method("on_media_item_transition", media_item, reason)

    @java_method("(Landroidx/media3/common/Tracks;)V")
    def onTracksChanged(self, tracks):
        self.call_player_method("on_tracks_changed", tracks)

    @java_method("(Landroidx/media3/common/MediaMetadata;)V")
    def onMediaMetadataChanged(self, media_metadata):
        self.call_player_method("on_media_metadata_changed", media_metadata)

    @java_method("(Landroidx/media3/common/MediaMetadata;)V")
    def onPlaylistMetadataChanged(self, playlist_metadata):
        self.call_player_method("on_playlist_metadata_changed", playlist_metadata)

    @java_method("(Z)V")
    def onIsLoadingChanged(self, is_loading):
        self.call_player_method("on_is_loading_changed", is_loading)

    @java_method("(Z)V")
    def onLoadingChanged(self, is_loading):
        self.call_player_method("on_loading_changed", is_loading)

    @java_method("(Landroidx/media3/common/Player$Commands;)V")
    def onAvailableCommandsChanged(self, commands):
        self.call_player_method("on_available_commands_changed", commands)

    @java_method("(Landroidx/media3/common/TrackSelectionParameters;)V")
    def onTrackSelectionParametersChanged(self, parameters):
        self.call_player_method("on_track_selection_parameters_changed", parameters)

    @java_method("(ZI)V")
    def onPlayerStateChanged(self, play_when_ready, playback_state):
        self.call_player_method("on_player_state_changed", play_when_ready, playback_state)

    @java_method("(I)V")
    def onPlaybackStateChanged(self, playback_state):
        self.call_player_method("on_playback_state_changed", playback_state)

    @java_method("(ZI)V")
    def onPlayWhenReadyChanged(self, play_when_ready, reason):
        self.call_player_method("on_play_when_ready_changed", play_when_ready, reason)

    @java_method("(I)V")
    def onPlaybackSuppressionReasonChanged(self, playback_suppression_reason):
        self.call_player_method("on_playback_suppression_reason_changed", playback_suppression_reason)

    @java_method("(Z)V")
    def onIsPlayingChanged(self, is_playing):
        self.call_player_method("on_is_playing_changed", is_playing)

    @java_method("(I)V")
    def onRepeatModeChanged(self, repeat_mode):
        self.call_player_method("on_repeat_mode_changed", repeat_mode)

    @java_method("(Z)V")
    def onShuffleModeEnabledChanged(self, shuffle_mode_enabled):
        self.call_player_method("on_shuffle_mode_enabled_changed", shuffle_mode_enabled)

    @java_method("(Landroidx/media3/common/PlaybackException;)V")
    def onPlayerError(self, error):
        self.call_player_method("on_player_error", error)

    @java_method("(Landroidx/media3/common/PlaybackException;)V")
    def onPlayerErrorChanged(self, error):
        self.call_player_method("on_player_error_changed", error)

    @java_method("(I)V", name="onPositionDiscontinuity")
    def onPositionDiscontinuityUnstableApi(self, reason):
        pass

    @java_method("(Landroidx/media3/common/Player$PositionInfo;Landroidx/media3/common/Player$PositionInfo;I)V")
    def onPositionDiscontinuity(self, old_position, new_position, reason):
        self.call_player_method("on_position_discontinuity", old_position, new_position, reason)

    @java_method("(Landroidx/media3/common/PlaybackParameters;)V")
    def onPlaybackParametersChanged(self, playback_parameters):
        self.call_player_method("on_playback_parameters_changed", playback_parameters)

    @java_method("(J)V")
    def onSeekBackIncrementChanged(self, seek_back_increment):
        self.call_player_method("on_seek_back_increment_changed", seek_back_increment)

    @java_method("(J)V")
    def onSeekForwardIncrementChanged(self, seek_forward_increment):
        self.call_player_method("on_seek_forward_increment_changed", seek_forward_increment)

    @java_method("(J)V")
    def onMaxSeekToPreviousPositionChanged(self, max_seek_to_previous_position):
        self.call_player_method("on_max_seek_to_previous_position_changed", max_seek_to_previous_position)

    @java_method("(I)V")
    def onAudioSessionIdChanged(self, audio_session_id):
        self.call_player_method("on_audio_session_id_changed", audio_session_id)

    @java_method("(Landroidx/media3/common/AudioAttributes;)V")
    def onAudioAttributesChanged(self, audio_attributes):
        self.call_player_method("on_audio_attributes_changed", audio_attributes)

    @java_method("(F)V")
    def onVolumeChanged(self, volume):
        self.call_player_method("on_volume_changed", volume)

    @java_method("(Z)V")
    def onSkipSilenceEnabledChanged(self, skip_silence_enabled):
        self.call_player_method("on_skip_silence_enabled_changed", skip_silence_enabled)

    @java_method("(Landroidx/media3/common/DeviceInfo;)V")
    def onDeviceInfoChanged(self, device_info):
        self.call_player_method("on_device_info_changed", device_info)

    @java_method("(IZ)V")
    def onDeviceVolumeChanged(self, volume, muted):
        self.call_player_method("on_device_volume_changed", volume, muted)

    @java_method("(Landroidx/media3/common/VideoSize;)V")
    def onVideoSizeChanged(self, video_size):
        self.call_player_method("on_video_size_changed", video_size)

    @java_method("(II)V")
    def onSurfaceSizeChanged(self, width, height):
        self.call_player_method("on_surface_size_changed", width, height)

    @java_method("()V")
    def onRenderedFirstFrame(self):
        self.call_player_method("on_rendered_first_frame")

    @java_method("(Ljava/util/List;)V")
    def onCues(self, cues):
        self.call_player_method("on_cues", cues)

    @java_method("Landroidx/media3/common/text/CueGroup;)V", name="onCues")
    def onCuesGroup(self, cue_group):
        self.call_player_method("on_cues_group", cue_group)

    @java_method("(Landroidx/media3/common/Metadata;)V")
    def onMetadata(self, metadata):
        self.call_player_method("on_metadata", metadata)
