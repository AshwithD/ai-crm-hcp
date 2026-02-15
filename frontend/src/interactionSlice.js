import { createSlice } from "@reduxjs/toolkit";

const initialState = {
  hcp_name: "",
  interaction_type: "Meeting",
  date: "",
  time: "",
  attendees: "",
  topics_discussed: [],
  materials_shared: [],
  samples_distributed: [],
  sentiment: "",
  outcomes: "",
  followups: [],
  last_interaction: "",
  last_topic: "",
  last_sentiment: "",
  compliance_issues: []
};

const interactionSlice = createSlice({
  name: "interaction",
  initialState,
  reducers: {
    mergeInteraction(state, action) {
      Object.entries(action.payload || {}).forEach(([k, v]) => {
        if (v !== null && v !== "" && !(Array.isArray(v) && v.length === 0)) {
          state[k] = v;
        }
      });
    },
  },
});

export const { mergeInteraction } = interactionSlice.actions;
export default interactionSlice.reducer;
